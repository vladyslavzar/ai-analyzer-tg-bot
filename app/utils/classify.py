"""Image classification utilities using torchvision ResNet18."""

import io
import os
import ssl
from typing import Optional

import certifi
import torch
from PIL import Image
from torchvision import models, transforms

# Fix SSL certificate issues on macOS
# Set SSL certificate path before any network requests
os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

# Load ResNet18 model and ImageNet class labels
_model: Optional[torch.nn.Module] = None
_class_names: Optional[list[str]] = None
_transform = transforms.Compose(
    [
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ]
)


def _load_imagenet_classes() -> list[str]:
    """Load ImageNet class names from PyTorch's official repository."""
    global _class_names
    if _class_names is None:
        import urllib.request
        
        # URL to ImageNet class names (standard mapping from PyTorch)
        imagenet_url = "https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt"
        
        try:
            # Download ImageNet class names
            with urllib.request.urlopen(imagenet_url, timeout=10) as response:
                class_names_text = response.read().decode('utf-8')
                _class_names = [line.strip() for line in class_names_text.strip().split('\n')]
            
            if len(_class_names) != 1000:
                raise ValueError(f"Expected 1000 classes, got {len(_class_names)}")
                
        except Exception as e:
            # Fallback: use a hardcoded subset if download fails
            print(f"Warning: Could not download ImageNet classes: {e}")
            print("Using fallback class names")
            
            # Create fallback with generic names
            _class_names = [f"class_{i}" for i in range(1000)]
            
            # Add some common class names we know
            common_classes = [
                "tench", "goldfish", "great white shark", "tiger shark", "hammerhead",
                "electric ray", "stingray", "cock", "hen", "ostrich",
                "brambling", "goldfinch", "house finch", "junco", "indigo bunting",
                "robin", "bulbul", "jay", "magpie", "chickadee",
            ]
            for i, name in enumerate(common_classes):
                if i < len(_class_names):
                    _class_names[i] = name

    return _class_names


def _load_model() -> torch.nn.Module:
    """Load and initialize ResNet18 model."""
    global _model
    if _model is None:
        # Fix SSL certificate issues for model download
        import ssl
        
        # Create SSL context with certifi certificates
        try:
            ssl_context = ssl.create_default_context(cafile=certifi.where())
            ssl._create_default_https_context = lambda: ssl_context
        except Exception:
            # Fallback: disable SSL verification (for local testing only)
            # WARNING: Not recommended for production
            ssl._create_default_https_context = ssl._create_unverified_context
        
        try:
            # Try to load pretrained weights
            _model = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)
        except Exception as e:
            # If download fails, try loading without weights (will use random weights)
            # This is a fallback for local testing
            try:
                _model = models.resnet18(weights=None)
                print(f"Warning: Could not download pretrained weights: {e}")
                print("Using model with random weights (classification may be inaccurate)")
            except Exception as e2:
                raise RuntimeError(f"Failed to load ResNet18 model: {e2}") from e2
        _model.eval()
    return _model


def classify_image(image_bytes: bytes, top_k: int = 3) -> list[tuple[str, float]]:
    """
    Classify an image using ResNet18.

    Args:
        image_bytes: Raw image bytes
        top_k: Number of top predictions to return (default: 3)

    Returns:
        List of tuples (predicted_label, confidence_score) sorted by confidence
    """
    try:
        # Load and preprocess image
        image = Image.open(io.BytesIO(image_bytes))
        if image.mode != "RGB":
            image = image.convert("RGB")

        # Apply transforms
        input_tensor = _transform(image).unsqueeze(0)

        # Get prediction
        model = _load_model()
        with torch.no_grad():
            output = model(input_tensor)
            probabilities = torch.nn.functional.softmax(output[0], dim=0)

        # Get top K predictions
        top_probs, top_indices = torch.topk(probabilities, min(top_k, 1000))
        
        # Get class labels
        class_names = _load_imagenet_classes()
        results = []
        
        for prob, idx in zip(top_probs, top_indices):
            class_idx = idx.item()
            confidence = float(prob)
            
            if class_idx < len(class_names):
                label = class_names[class_idx]
            else:
                label = f"class_{class_idx}"
            
            results.append((label, confidence))
        
        return results

    except Exception as e:
        raise ValueError(f"Failed to classify image: {str(e)}") from e


# Prediction interface for Cog ⚙️
# https://github.com/replicate/cog/blob/main/docs/python.md

from typing import List
from cog import BasePredictor, BaseModel, Input, Path

import torch
import allin1
import os 

class Predictor(BasePredictor):
    def setup(self):
        """Load the model into memory to make running multiple predictions efficient"""
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

    def predict(
        self,
        music_input: Path = Input(
            description="An audio file input to analyze.",
            default=None,
        ),
        visualize: bool = Input(
            description="Save visualizations",
            default=False,
        ),
        sonify: bool = Input(
            description="Save sonifications",
            default=False,
        ),
        activ: bool = Input(
            description="Save frame-level raw activations from sigmoid and softmax",
            default=False,
        ),
        embed: bool = Input(
            description="Save frame-level embeddings",
            default=False,
        ),
        demux: bool = Input(
            description="Save demuxed audio files",
            default=False,
        ),
        model: str = Input(
            description="Name of the pretrained model to use",
            default="harmonix-all",
            choices=["harmonix-all", "harmonix-fold0", "harmonix-fold1", "harmonix-fold2", "harmonix-fold3", "harmonix-fold4", "harmonix-fold5", "harmonix-fold6", "harmonix-fold7"]
        ),
        include_activations: bool = Input(
            description="Whether to include activations in the analysis results or not.",
            default=False
        ),
        include_embeddings: bool = Input(
            description="Whether to include embeddings in the analysis results or not.",
            default=False,
        ),
    ) -> List[Path]:

        if not music_input:
            raise ValueError("Must provide `music_input`.")

        if os.path.isdir('demix'):
            import shutil
            shutil.rmtree('demix')
        if os.path.isdir('spec'):
            import shutil
            shutil.rmtree('spec')
        if os.path.isdir('output'):
            import shutil
            shutil.rmtree('output')

        # Music Structure Analysis
        music_input_analysis = allin1.analyze(paths=music_input, out_dir='output', visualize=visualize, sonify=sonify, model=model, device=self.device, include_activations=include_activations, include_embeddings=include_embeddings, keep_byproducts=demux)

        output_dir = []

        for dirpath, dirnames, filenames in os.walk("output"):
            for filename in [f for f in filenames if f.rsplit('.', 1)[-1] == "json"]:
                json_dir = os.path.join(dirpath, filename)
        output_dir.append(Path(json_dir))

        if visualize:
            for dirpath, dirnames, filenames in os.walk("viz"):
                for filename in [f for f in filenames if f.rsplit('.', 1)[-1] == "pdf"]:
                    visualization_dir = os.path.join(dirpath, filename)
                    import fitz
                    doc = fitz.open(str(visualization_dir))
                    for i, page in enumerate(doc):
                        img = page.get_pixmap()
                        img_dir = str(visualization_dir).rsplit('.',1)[0]+'.png'
                        img.save(img_dir)
                        break
            output_dir.append(Path(img_dir))

        if sonify:
            for dirpath, dirnames, filenames in os.walk("sonif"):
                for filename in [f for f in filenames if f.rsplit('.', 1)[-1] == "mp3"]:
                    sonification_dir = os.path.join(dirpath, filename)
            output_dir.append(Path(sonification_dir))
        
        if demux:
             # Create output/demix directory
            demux_dir = Path('output/demix')
            demux_dir.mkdir(parents=True, exist_ok=True)
    
            # Find and copy all .wav files from nested structure
            htdemucs_dir = Path('demix/htdemucs')
            if htdemucs_dir.is_dir():
                for subdir in htdemucs_dir.iterdir():
                    if subdir.is_dir():  # tmp7rov49plfile or similar temp dirs
                        for wav_file in subdir.glob('*.wav'):
                            import shutil
                            destination = demux_dir / wav_file.name
                            shutil.copy2(wav_file, destination)
                            output_dir.append(destination)      

        return output_dir
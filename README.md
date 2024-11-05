# Cog Implementation of All-In-One Music Structure Analyzer

[![Replicate](https://replicate.com/cwalo/all-in-one-music-structure-analysis/badge)](https://replicate.com/cwalo/all-in-one-music-structure-analysis) 

[All-In-One Music Structure Analysis](https://replicate.com/cwalo/all-in-one-music-structure-analysis) is a package provides models for music structure analysis, predicting:

1. Tempo (BPM) 
2. Beats
3. Downbeats
4. Functional segment boundaries
5. Functional segment labels (e.g., intro, verse, chorus, bridge, outro)
6. Demux/demix music into its parts (drums, bass, vocals, other)

For more information about this model, see [here](https://github.com/mir-aidj/all-in-one).

You can demo this model or learn how to use it with Replicate's API [here](https://replicate.com/cwalo/all-in-one-music-structure-analysis). 

## Prediction
### Default Model
- In this repository, the default prediction model is configured as the melody model.
- After completing the fine-tuning process from this repository, the trained model weights will be loaded into your own model repository on Replicate.

# Run with Cog

[Cog](https://github.com/replicate/cog) is an open-source tool that packages machine learning models in a standard, production-ready container. 
You can deploy your packaged model to your own infrastructure, or to [Replicate](https://replicate.com/), where users can interact with it via web interface or API.

## Prerequisites 

**Cog.** Follow these [instructions](https://github.com/replicate/cog#install) to install Cog, or just run: 

```
sudo curl -o /usr/local/bin/cog -L "https://github.com/replicate/cog/releases/latest/download/cog_$(uname -s)_$(uname -m)"
sudo chmod +x /usr/local/bin/cog
```

Note, to use Cog, you'll also need an installation of [Docker](https://docs.docker.com/get-docker/).

* **GPU machine.** For best performance, you'll need a Linux machine with an NVIDIA GPU attached and the [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#docker) installed. If you don't already have access to a machine with a GPU, check out our [guide to getting a 
GPU machine](https://replicate.com/docs/guides/get-a-gpu-machine).

* To use a CPU instead, update the build section of `cog.yaml`. When using a CPU, we recommend using much shorter input files, otherwise prediction will take considerably longer. 

```yaml
build:
  # set false to use the CPU if a GPU is not available
  gpu: true 
  cuda: "11.7"
```

## Step 1. Clone this repository

```sh
git clone https://github.com/cwalo/cog-all-in-one
```

## Step 2. Run the model

To run the model, you need a local copy of the model's Docker image. You can satisfy this requirement by specifying the image ID in your call to `predict` like:

```
cog predict r8.im/cwalo/all-in-one-music-structure-analysis@sha256:001b4137be6ac67bdc28cb5cffacf128b874f530258d033de23121e785cb7290 -i music_input=@/your/audio/file.wav
```

For more information, see the Cog section [here](https://replicate.com/cwalo/all-in-one-music-structure-analysis/api)

Alternatively, you can build the image yourself, either by running `cog build` or by letting `cog predict` trigger the build process implicitly. For example, the following will trigger the build process and then execute prediction: 

```
cog predict -i music_input=@/your/audio/file.wav
```

Note, the first time you run `cog predict`, model weights and other requisite assets will be downloaded if they're not available locally. This download only needs to be executed once.

# Run on replicate

## Step 1. Ensure that all assets are available locally

If you haven't already, you should ensure that your model runs locally with `cog predict`. This will guarantee that all assets are accessible. E.g., run: 

```
cog predict -i audio_input=@/your/audio/file.wav
```

## Step 2. Create a model on Replicate.

Go to [replicate.com/create](https://replicate.com/create) to create a Replicate model. If you want to keep the model private, make sure to specify "private".

## Step 3. Configure the model's hardware

Replicate supports running models on variety of CPU and GPU configurations. 

Click on the "Settings" tab on your model page, scroll down to "GPU hardware", and select "T4". Then click "Save".

## Step 4: Push the model to Replicate


Log in to Replicate:

```
cog login
```

Push the contents of your current directory to Replicate, using the model name you specified in step 1:

```
cog push r8.im/username/modelname
```

[Learn more about pushing models to Replicate.](https://replicate.com/docs/guides/push-a-model)

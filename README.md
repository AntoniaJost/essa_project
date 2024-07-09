# Earth System Science and the Anthropocene Project Report

## Overview
This project contains the scripts used for the Tutorial Project about Resilience Measures of the course "Earth System Science & Anthropocene". It consists of three parts. The first one assesses the resilience of the Amazon rainforest using a simple vegetation model. It demonstrates how varying initial conditions and aridity levels impact the temporal evolution of the forest cover and explores several resilience measures, including an evaluation of the stability of the forest ecosystem. Moreover, the project covers several key functionalities such as local stability analysis (including characteristic return time calculations), and global stability assessments (like basin stability). The second part allows an interactive inspection of the plots from the previous part. Lastly, the third part is an in-depth exploration of the dynamics of the climate-biosphere-system. For different initial conditions, following the RCP scenarios until 2100, the resilience of the system against direct human impact on biodiversity is evaluated. This is done mainly by focussing on the return time to acceptable global temperatures.

## Project Structure

```
.
├── input/                                                  # Directory for input data files
├── output_plots/                                           # Directory for output plots
├── Amazon_Rainforest_Model_and_Resilience_Measures.ipynb   # Jupyter notebook with initial model and resilience measures
├── Climate_Biosphere_Model.ipynb                           # Jupyter notebook with vegetation model
├── LICENSE                                                 # License file
├── README.md                                               # Project description and instructions (this file)
├── 3d_amazon_rainforest_model.py                           # Python script with model functions and Dash app
└── requirements.txt                                        # Python dependencies
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/essa_project.git
cd essa_project
```

2. Create and activate the conda environment:

```bash
conda env create -f environment.yml
conda activate essa_model
```

## Usage

### Running the Model

1. **Jupyter Notebooks**:
   - Open any of the Jupyter notebooks using Jupyter Lab or Jupyter Notebook.
   - Select a kernel.
   - Run the cells to execute the models and generate plots.

2. **Python Scripts**:
   - `3d_amazon_rainforest_model.py`: Contains (the same) functions for vegetation model calculations and a Dash app for interactive exploration.

### Interactive Dash Application

A Dash application is included for interactive exploration of the model:

1. Run the Dash app:

```bash
python 3d_amazon_rainforest_model.py
```

2. Open your web browser and navigate to `http://127.0.0.1:8050` to view the interactive application.

### Key Features of the Dash App

- **Vegetation Cover over Time and Aridity**: Visualise how forest cover changes over time with varying aridity.
- **Global Return Time Analysis**: Explore the time steps required for the forest to return to equilibrium after a perturbation.
- **Characteristic Return Time**: Analyse the characteristic return time for both forest and savanna states based on different saturation and death rates.

## Key Concepts

### Vegetation Model

Levin’s widely accepted vegetation model:

$$ 
\frac{dC}{dt} = 
\begin{cases}   
    r(1 − C)C − x C & \text{if } C > C_{crit} \\
    −x C & \text{if } C < C_{crit}
\end{cases}
$$

- **C**: Forest cover
- **r**: Saturation rate
- **x**: Death rate

### Stability Analysis

- **Equilibrium States**: Stable and unstable states of forest cover.
- **Characteristic Return Time**: Time taken for a perturbation to decay to equilibrium.
- **Basin Stability**: Probability of returning to equilibrium after random perturbations.

### Climate-Biosphere Model

The theoretical background of the climate-biosphere model that is implemented can be found in Lade SJ et al. (2019). Potential feedbacks between loss of biosphere
integrity and climate change. _Global Sustainability_ **2**, e21, 1–15. https://doi.org/10.1017/sus.2019.18 .

## License

This project is licensed under the GNU Affero General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Contributors

- **Sophia Künzig** - <sophia.kuenzig@uni-potsdam.de>
- **Rike Mühlhaus** - <ulrike.muehlhaus@uni-potsdam.de>
- **Antonia Jost**  - <antonia.jost@uni-potsdam.de>


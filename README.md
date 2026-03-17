<img src="layers.png" alt="layers.png" width="800"/>

### `Data pre-processing and analysis of the results obtained in Pix4Dfields`
This repository contains mutlispectral data, and also all preprocessing and evaluation code used in the study 
“Impact of Biostimulants Foliar Applications on Primocane Raspberries Assessed Using UAV-Based Multispectral Imaging”.

<p align="justify">The "codes" folder contains all the scripts and algorithms used to analyze and pre-process the results obtained in Pix4Dfields. The "data" folder contains the results obtained in Pix4Dfields, and the "results_csv" and "results_graphs" folders contain the final results of their analysis.</p>

## Citation
If you use this repository, please cite:
Will be added after publication

<p align="justify">Multispectral imaging generates large volumes of data that necessitate advanced analytical approaches. Pix4Dfields software enables the calculation of vegetation indices for user-defined regions, together with associated standard deviation values, which constitute a key input for subsequent analyses. Although this transformation reduces raw imagery to more interpretable quantitative indicators, it results in a considerable number of outputs, the correct interpretation of which becomes particularly important in long-term experimental studies.</p>

<p align="justify">In the analysis of vegetation indices obtained from Pix4Dfields across multiple time points, an initial data preprocessing step may be applied, including, where appropriate, exploratory data analysis (EDA). This approach is particularly valuable when datasets are generated using different acquisition or processing settings, such as varying ground sampling distances (GSD) or annotation methods, as it facilitates the identification of the most consistent outputs for further interpretation. Nevertheless, the application of this procedure is not obligatory in all analytical contexts. </p>

<p align="center">
  <img src="results_analysis_scheme.png" alt="results_analysis_scheme.png" width="800"/>
</p>

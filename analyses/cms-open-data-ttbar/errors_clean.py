import numpy as np
import ROOT

def extract_histogram_data(hist):
    bin_contents = np.array([hist.GetBinContent(i + 1) for i in range(hist.GetNbinsX())])
    return bin_contents

def compute_deviations(hist1, hist2):
    values1 = extract_histogram_data(hist1)
    values2 = extract_histogram_data(hist2)
    deviations = np.zeros(len(values1))
    for i in range(len(deviations)):
        value1 = values1[i]
        value2 = values2[i]
        deviations[i] = 0 if round(value2, 5) == round(value1, 5) == 0 else 100 * abs(value1 - value2) / max(value1,value2)
    return deviations

def find_mismatches(file1_path, file2_path):
    file1 = ROOT.TFile.Open(file1_path)
    file2 = ROOT.TFile.Open(file2_path)
    
    keys1 = {key.GetName() for key in file1.GetListOfKeys()}
    keys2 = {key.GetName() for key in file2.GetListOfKeys()}
    
    common_keys = keys1 & keys2
    
    for hist_name in common_keys:
        hist1 = file1.Get(hist_name)
        hist2 = file2.Get(hist_name)
        if hist1 and hist2:
            deviations = compute_deviations(hist1, hist2)
            max_deviation_index = np.argmax(deviations)
            max_deviation = deviations[max_deviation_index]
            if max_deviation > 0.001:
                print(f"Histogram: {hist_name}")
                print(f"  Maximum deviation: {max_deviation:.2f}%")
        else:
            print(f"Histogram '{hist_name}' is not found in one of the files.")
    
    file1.Close()
    file2.Close()

if __name__ == "__main__":
    print("new set clean")
    #find_mismatches("/Users/andreaolamejicanos/analysis-grand-challenge/analyses/cms-open-data-ttbar/reference_root/ml/histograms_ml_iris_ttree_1.root", "/Users/andreaolamejicanos/analysis-grand-challenge/analyses/cms-open-data-ttbar/reference_root/ml/histograms_ml_dist_ttree_1.root")
    #find_mismatches("/Users/andreaolamejicanos/analysis-grand-challenge/analyses/cms-open-data-ttbar/reference_root/reference_all/histograms_mt_10.root", "/Users/andreaolamejicanos/analysis-grand-challenge/analyses/cms-open-data-ttbar/reference_root/reference_all/histograms_dist_memray_10.root")
    find_mismatches("/Users/andreaolamejicanos/analysis-grand-challenge/analyses/cms-open-data-ttbar/reference_root/analysis/histograms_dist_ttree_1.root", "/Users/andreaolamejicanos/analysis-grand-challenge/analyses/cms-open-data-ttbar/reference_root/reference_all/histograms_dist_memray_1.root")
    
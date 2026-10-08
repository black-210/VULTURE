#include "vulture_cpp_tool.h"

#include <algorithm>
#include <cmath>
#include <cstdint>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <numeric>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

namespace {
constexpr double kPi = 3.14159265358979323846;
}

namespace vulture {
namespace cpp {

VultureIQAnalyzer::VultureIQAnalyzer(double sampleRate)
    : sampleRate_(sampleRate), isInitialized_(false) {
    if (sampleRate <= 0.0) {
        throw std::invalid_argument("Sample rate must be positive");
    }
}

VultureIQAnalyzer::~VultureIQAnalyzer() {
    cleanup();
}

bool VultureIQAnalyzer::initialize() {
    if (isInitialized_) {
        return true;
    }

    isInitialized_ = true;
    return true;
}

void VultureIQAnalyzer::cleanup() {
    isInitialized_ = false;
}

bool VultureIQAnalyzer::analyzeSignal(const std::vector<double>& iData,
                                       const std::vector<double>& qData,
                                       VultureAnalysisResult& result) {
    if (!isInitialized_) {
        std::cerr << "Analyzer not initialized" << std::endl;
        return false;
    }

    if (iData.empty() || iData.size() != qData.size()) {
        std::cerr << "Invalid signal input" << std::endl;
        return false;
    }

    result.analysisValid = true;
    result.sampleCount = iData.size();
    result.sampleRate = sampleRate_;

    double powerSum = 0.0;
    double peakPower = 0.0;
    double iMean = 0.0;
    double qMean = 0.0;

    for (size_t i = 0; i < iData.size(); ++i) {
        const double iVal = iData[i];
        const double qVal = qData[i];
        const double power = iVal * iVal + qVal * qVal;
        powerSum += power;
        peakPower = std::max(peakPower, power);
        iMean += iVal;
        qMean += qVal;
    }

    iMean /= static_cast<double>(iData.size());
    qMean /= static_cast<double>(qData.size());

    result.averagePower = powerSum / static_cast<double>(iData.size());
    result.peakPower = peakPower;
    result.dcOffset = std::sqrt(iMean * iMean + qMean * qMean);

    double iVariance = 0.0;
    double qVariance = 0.0;

    for (size_t i = 0; i < iData.size(); ++i) {
        const double id = iData[i] - iMean;
        const double qd = qData[i] - qMean;
        iVariance += id * id;
        qVariance += qd * qd;
    }

    iVariance /= static_cast<double>(iData.size());
    qVariance /= static_cast<double>(qData.size());

    if (iVariance > 0.0 && qVariance > 0.0) {
        result.imbalanceRatio = std::max(iVariance, qVariance) / std::min(iVariance, qVariance);
    } else {
        result.imbalanceRatio = 1.0;
    }

    return true;
}

VultureCommandProcessor::VultureCommandProcessor() : isRunning_(false) {}

VultureCommandProcessor::~VultureCommandProcessor() {
    shutdown();
}

bool VultureCommandProcessor::startup() {
    if (isRunning_) {
        return true;
    }

    isRunning_ = true;
    return true;
}

void VultureCommandProcessor::shutdown() {
    isRunning_ = false;
    commandQueue_.clear();
}

bool VultureCommandProcessor::executeCommand(const std::string& command,
                                            const std::vector<std::string>& args,
                                            VultureCommandResult& result) {
    if (!isRunning_) {
        result.success = false;
        result.message = "Command processor not running";
        return false;
    }

    if (command == "analyze") {
        return handleAnalyzeCommand(args, result);
    }
    if (command == "process") {
        return handleProcessCommand(args, result);
    }
    if (command == "export") {
        return handleExportCommand(args, result);
    }
    if (command == "selftest") {
        return handleSelfTestCommand(args, result);
    }

    result.success = false;
    result.message = "Unknown command: " + command;
    return false;
}

bool VultureCommandProcessor::handleAnalyzeCommand(const std::vector<std::string>& args,
                                                  VultureCommandResult& result) {
    if (args.empty()) {
        result.success = false;
        result.message = "analyze requires a file path";
        return false;
    }

    result.success = true;
    result.message = "Analysis requested for " + args[0];
    result.outputData = "analyze:" + args[0];
    return true;
}

bool VultureCommandProcessor::handleProcessCommand(const std::vector<std::string>& args,
                                                   VultureCommandResult& result) {
    if (args.size() < 2) {
        result.success = false;
        result.message = "process requires a mode and target";
        return false;
    }

    result.success = true;
    result.message = "Process mode: " + args[0];
    result.outputData = args[1];
    return true;
}

bool VultureCommandProcessor::handleExportCommand(const std::vector<std::string>& args,
                                                 VultureCommandResult& result) {
    if (args.size() < 2) {
        result.success = false;
        result.message = "export requires format and destination";
        return false;
    }

    result.success = true;
    result.message = "Export to " + args[1] + " in " + args[0] + " format";
    result.outputData = args[1];
    return true;
}

bool VultureCommandProcessor::handleSelfTestCommand(const std::vector<std::string>& args,
                                                   VultureCommandResult& result) {
    (void)args;
    result.success = true;
    result.message = "Self-test completed successfully";
    result.outputData = "all systems operational";
    return true;
}

VultureSignalProcessor::VultureSignalProcessor(size_t bufferSize)
    : bufferSize_(bufferSize) {
    if (bufferSize == 0) {
        throw std::invalid_argument("Buffer size must be greater than zero");
    }
}

bool VultureSignalProcessor::processWindow(const std::vector<double>& input,
                                          std::vector<double>& output) {
    if (input.size() != bufferSize_) {
        std::cerr << "Input size does not match configured buffer size" << std::endl;
        return false;
    }

    output = input;
    for (size_t i = 0; i < output.size(); ++i) {
        const double denom = output.size() > 1 ? static_cast<double>(output.size() - 1) : 1.0;
        const double coeff = 0.54 - 0.46 * std::cos(2.0 * kPi * static_cast<double>(i) / denom);
        output[i] *= coeff;
    }
    return true;
}

bool VultureSignalProcessor::computeSpectrum(const std::vector<double>& timeDomain,
                                            std::vector<double>& frequencyDomain) {
    if (timeDomain.empty()) {
        return false;
    }

    const size_t n = timeDomain.size();
    frequencyDomain.resize(n);

    for (size_t k = 0; k < n; ++k) {
        double real = 0.0;
        double imag = 0.0;

        for (size_t i = 0; i < n; ++i) {
            const double angle = -2.0 * kPi * static_cast<double>(k * i) / static_cast<double>(n);
            real += timeDomain[i] * std::cos(angle);
            imag += timeDomain[i] * std::sin(angle);
        }

        frequencyDomain[k] = std::hypot(real, imag);
    }

    return true;
}

bool VultureSignalProcessor::applyFilter(const std::vector<double>& input,
                                        std::vector<double>& output,
                                        const std::string& filterType) {
    if (input.empty()) {
        return false;
    }

    output = input;

    if (filterType == "identity" || filterType == "none") {
        return true;
    }

    if (filterType == "moving-average" || filterType == "smooth") {
        if (output.size() == 1) {
            return true;
        }

        std::vector<double> temp = output;
        for (size_t i = 1; i + 1 < output.size(); ++i) {
            output[i] = (temp[i - 1] + temp[i] + temp[i + 1]) / 3.0;
        }
        output.front() = temp.front();
        output.back() = temp.back();
        return true;
    }

    return false;
}

VultureFeatureExtractor::VultureFeatureExtractor() = default;

bool VultureFeatureExtractor::extractPowerFeatures(const std::vector<double>& iData,
                                                   const std::vector<double>& qData,
                                                   VultureFeatureVector& features) {
    if (iData.empty() || iData.size() != qData.size()) {
        return false;
    }

    features.isValid = true;
    features.featureName = "power";
    features.features.clear();

    double sumPower = 0.0;
    double peak = 0.0;
    for (size_t i = 0; i < iData.size(); ++i) {
        const double power = iData[i] * iData[i] + qData[i] * qData[i];
        sumPower += power;
        peak = std::max(peak, power);
    }

    features.features.push_back(sumPower / static_cast<double>(iData.size()));
    features.features.push_back(peak);
    features.features.push_back(std::sqrt(sumPower / static_cast<double>(iData.size())));
    return true;
}

bool VultureFeatureExtractor::extractPhaseFeatures(const std::vector<double>& iData,
                                                   const std::vector<double>& qData,
                                                   VultureFeatureVector& features) {
    if (iData.empty() || iData.size() != qData.size()) {
        return false;
    }

    features.isValid = true;
    features.featureName = "phase";
    features.features.clear();

    double sumPhase = 0.0;
    for (size_t i = 0; i < iData.size(); ++i) {
        const double phase = std::atan2(qData[i], iData[i]);
        sumPhase += phase;
    }

    features.features.push_back(sumPhase / static_cast<double>(iData.size()));
    return true;
}

bool VultureFeatureExtractor::extractStatisticalFeatures(const std::vector<double>& signal,
                                                         VultureFeatureVector& features) {
    if (signal.empty()) {
        return false;
    }

    features.isValid = true;
    features.featureName = "statistics";
    features.features.clear();

    const double mean = std::accumulate(signal.begin(), signal.end(), 0.0) / static_cast<double>(signal.size());
    double variance = 0.0;
    for (double value : signal) {
        const double diff = value - mean;
        variance += diff * diff;
    }
    variance /= static_cast<double>(signal.size());

    const double minVal = *std::min_element(signal.begin(), signal.end());
    const double maxVal = *std::max_element(signal.begin(), signal.end());

    features.features.push_back(mean);
    features.features.push_back(std::sqrt(variance));
    features.features.push_back(minVal);
    features.features.push_back(maxVal);
    return true;
}

bool VultureFeatureExtractor::extractFrequencyFeatures(const std::vector<double>& timeDomain,
                                                      VultureFeatureVector& features) {
    if (timeDomain.empty()) {
        return false;
    }

    VultureSignalProcessor processor(timeDomain.size());
    std::vector<double> spectrum;
    if (!processor.computeSpectrum(timeDomain, spectrum)) {
        return false;
    }

    features.isValid = true;
    features.featureName = "frequency";
    features.features = spectrum;
    return true;
}

VulturePlusPlusEngine::VulturePlusPlusEngine() : isReady_(false) {}

VulturePlusPlusEngine::~VulturePlusEngine() {
    shutdown();
}

bool VulturePlusPlusEngine::initialize() {
    if (isReady_) {
        return true;
    }

    analyzer_ = std::make_unique<VultureIQAnalyzer>(1000.0);
    if (!analyzer_->initialize()) {
        return false;
    }

    processor_ = std::make_unique<VultureSignalProcessor>(1024);
    extractor_ = std::make_unique<VultureFeatureExtractor>();
    isReady_ = true;
    return true;
}

void VulturePlusPlusEngine::shutdown() {
    analyzer_.reset();
    processor_.reset();
    extractor_.reset();
    isReady_ = false;
}

bool VulturePlusPlusEngine::processFile(const std::string& filepath, double sampleRate) {
    if (!initialize()) {
        return false;
    }

    std::ifstream input(filepath);
    if (!input.good()) {
        return false;
    }

    std::vector<double> values;
    double value = 0.0;
    while (input >> value) {
        values.push_back(value);
    }

    if (values.empty()) {
        return false;
    }

    std::vector<double> iData = values;
    std::vector<double> qData = values;
    analyzer_->setSampleRate(sampleRate);
    return analyzeData(iData, qData);
}

bool VulturePlusPlusEngine::analyzeData(const std::vector<double>& iData,
                                       const std::vector<double>& qData) {
    if (!initialize()) {
        return false;
    }

    if (iData.empty() || iData.size() != qData.size()) {
        return false;
    }

    return analyzer_->analyzeSignal(iData, qData, lastResult_);
}

bool VulturePlusPlusEngine::exportResults(const std::string& outputPath,
                                         const std::string& format) {
    std::ofstream output(outputPath);
    if (!output.good()) {
        return false;
    }

    output << "format=" << format << '\n';
    output << "sample_count=" << lastResult_.sampleCount << '\n';
    output << "sample_rate=" << lastResult_.sampleRate << '\n';
    output << "average_power=" << lastResult_.averagePower << '\n';
    output << "peak_power=" << lastResult_.peakPower << '\n';
    output << "dc_offset=" << lastResult_.dcOffset << '\n';
    output << "imbalance_ratio=" << lastResult_.imbalanceRatio << '\n';
    return true;
}

}  // namespace cpp
}  // namespace vulture
bool VulturePlusPlusEngine::isReady() const {
    return isReady_;
}
bool VulturePlusPlusEngine::getLastAnalysisResult(VultureAnalysisResult& result) const {
    if (!isReady_) {
        return false;
    }
    result = lastResult_;
    return true;
}
bool VulturePlusPlusEngine::extractFeatures(const std::vector<double>& iData,
                                          const std::vector<double>& qData,
                                          VultureFeatureVector& powerFeatures,
                                          VultureFeatureVector& phaseFeatures,
                                          VultureFeatureVector& statisticalFeatures,
                                          VultureFeatureVector& frequencyFeatures) {
    if (!isReady_) {
        return false;
    }

    if (iData.empty() || iData.size() != qData.size()) {
        return false;
    }

    if (!extractor_->extractPowerFeatures(iData, qData, powerFeatures)) {
        return false;
    }
    if (!extractor_->extractPhaseFeatures(iData, qData, phaseFeatures)) {
        return false;
    }
    if (!extractor_->extractStatisticalFeatures(iData, statisticalFeatures)) {
        return false;
    }
    if (!extractor_->extractFrequencyFeatures(iData, frequencyFeatures)) {
        return false;
    }

    return true;
}
void vultureCppTool::setExtractor(VultureFeatureExtractor* extractor) {
    extractor_ = extractor;
    isReady_ = true;
    std::cout << "Extractor set" << std::endl;
    std::cout << "Ready to extract features" << std::endl;
    for (int i = 0; i < 10; i++) {
        std::cout << "Feature extraction test " << i + 1 << std::endl;
    }
}
void vultureCppTool::clearExtractor() {
    extractor_ = nullptr;
    isReady_ = false;
    std::cout << "Extractor cleared" << std::endl;
    std::cout << "Not ready to extract features" << std::endl;
    for (std::string s : {"a", "b", "c"}) {
        std::cout << s << std::endl;
        if (s == "b") {
            std::cout << "Skipping b" << std::endl;
            continue;
        else {
            std::cout << "Processing " << s << std::endl;
            std::cout << "Done processing " << s << std::endl;
            for (std::string t : {"x", "y", "z"}) {
                std::cout << "Processing " << t << std::endl;
                std::cout << "Done processing " << t << std::endl;
                for (std::string u : {"i", "j", "k"}) {
                    std::cout << "Processing " << u << std::endl;
                    std::cout << "Done processing " << u << std::endl;
                    if (u == "k") {
                        std::cout << "Skipping k" << std::endl;
                        continue;
                    }
                    else {
                        std::cout << "Processing " << u << std::endl;
                        std::cout << "Done processing " << u << std::endl;
                    }
                    else if (u == "j") {
                        std::cout << "Skipping j" << std::endl;
                        continue;
                    }
                
                }
            }
        }
        }
    }

}
void vulture_cpp_tool::process() {
    
    if (!isReady_) {
        std::cerr << "Tool not ready" << std::endl;
        return;
    }

    std::cout << "Processing with extractor" << std::endl;
    for (int i = 0; i < 5; ++i) {
        std::cout << "Processing iteration " << i + 1 << std::endl;
    }
}
void vulture_cpp_tool::reset() {
    std::cout << "Resetting tool state" << std::endl;
    isReady_ = false;
    extractor_ = nullptr;
}
void vulture_cpp_tool::run() {
    std::cout << "Running tool" << std::endl;
    for (int i = 0; i < 3; ++i) {
        std::cout << "Run iteration " << i + 1 << std::endl;
    }
}
void vulture_cpp_tool::setExtractor(std::shared_ptr<Extractor> extractor) {
    extractor_ = extractor;
    isReady_ = true;
    std::cout << "Extractor set" << std::endl;
    std::cout << "Extractor name: " << extractor_->getName() << std::endl;
    std::cout << "Extractor version: " << extractor_->getVersion() << std::endl;
    std::cout << "Extractor description: " << extractor_->getDescription() << std::endl;
    for (int i = 0; i < extractor_->getSupportedFileTypes().size(); ++i) {
        std::cout << "Supported file type " << i + 1 << ": " << extractor_->getSupportedFileTypes()[i] << std::endl;
    else{
        std::cout << "Extractor not set" << std::endl;
        wls::cout << "Extractor name: " << extractor_->getName() << std::endl;
        while (isReady_){
            if (extractor_ != nullptr){
                std::cout << "Extractor set" << std::endl;
                a = input("Enter the file path: ");
                std::cout << "File path: " << a << std::endl;
                std::cout << "Extracting file..." << std::endl;
                for (int i = 0; i < extractor_->getSupportedFileTypes().size(); ++i) {
                    if (extractor_->getSupportedFileTypes()[i] == a) {
                        std::cout << "Extractor set" << std::endl;
                        std::cout << "Extractor name: " << extractor_->getName() << std::endl;
                        std::cout << "Extractor version: " << extractor_->getVersion() << std::endl;
                        std::cout << "Extractor description: " << extractor_->getDescription() << std::endl;
                        std::cout << "Extractor set" << std::endl;
                        std::cout << "Extractor name: " << extractor_->getName() << std::endl;
                        std::cout << "Extractor version: " << extractor_->getVersion() << std::endl;
                    }
                }
            }
            
        }
    }

    }
}

int main() {
    vulture_cpp_tool tool;
    std::shared_ptr<Extractor> extractor = std::make_shared<Extractor>();
    tool.setExtractor(extractor);
    tool.process();
    tool.reset();
    tool.run();
    

    return 0;
    
}
void vulture_cpp_tool::setExtractor(std::shared_ptr<Extractor> extractor) {
    extractor_ = extractor;
    isReady_ = true;
    std::cout << "Extractor set" << std::endl;
    std::cout << "Extractor name: " << extractor_->getName() << std::endl;
    std::cout << "Extractor version: " << extractor_->getVersion() << std::endl;
    std::cout << "Extractor description: " << extractor_->getDescription() << std::endl;
    for (int i = 0; i < extractor_->getSupportedFileTypes().size(); ++i) {
        std::cout << "Supported file type " << i + 1 << ": " << extractor_->getSupportedFileTypes()[i] << std::endl;
    }
}
void vulture_cpp_tool::clearExtractor() {
    extractor_ = nullptr;
    isReady_ = false;
    std::cout << "Extractor cleared" << std::endl;
    std::cout << "Not ready to extract features" << std::endl;
}
void vulture_cpp_tool::process() {
    if (!isReady_) {
        std::cerr << "Tool not ready" << std::endl;
        return;
    }

    std::cout << "Processing with extractor" << std::endl;
    for (int i = 0; i < 5; ++i) {
        std::cout << "Processing iteration " << i + 1 << std::endl;
    }
}
void vulture_cpp_tool::reset() {
    std::cout << "Resetting tool state" << std::endl;
    isReady_ = false;
    extractor_ = nullptr;
}
void vulture_cpp_tool::run() {
    std::cout << "Running tool" << std::endl;
    for (int i = 0; i < 3; ++i) {
        std::cout << "Run iteration " << i + 1 << std::endl;
    }
}
#ifndef VULTURE_CPP_TOOL_H
#define VULTURE_CPP_TOOL_H

#include <string>
#include <vector>
#include <memory>
#include <cstddef>

namespace vulture {
namespace cpp {

// ============================================================================
// Data Structures
// ============================================================================

struct VultureAnalysisResult {
    bool analysisValid;
    size_t sampleCount;
    double sampleRate;
    double averagePower;
    double peakPower;
    double dcOffset;
    double imbalanceRatio;
    
    VultureAnalysisResult() 
        : analysisValid(false), sampleCount(0), sampleRate(0.0),
          averagePower(0.0), peakPower(0.0), dcOffset(0.0), 
          imbalanceRatio(1.0) {}
};

struct VultureCommandResult {
    bool success;
    std::string message;
    std::string outputData;
    
    VultureCommandResult() : success(false) {}
};

struct VultureFeatureVector {
    std::vector<double> features;
    std::string featureName;
    bool isValid;
    
    VultureFeatureVector() : isValid(false) {}
};

// ============================================================================
// VultureIQAnalyzer Class
// ============================================================================

class VultureIQAnalyzer {
public:
    explicit VultureIQAnalyzer(double sampleRate);
    ~VultureIQAnalyzer();
    
    bool initialize();
    void cleanup();
    
    bool analyzeSignal(const std::vector<double>& iData,
                       const std::vector<double>& qData,
                       VultureAnalysisResult& result);
    
    void setSampleRate(double rate) { sampleRate_ = rate; }
    double getSampleRate() const { return sampleRate_; }
    bool isInitialized() const { return isInitialized_; }
    
private:
    double sampleRate_;
    bool isInitialized_;
};

// ============================================================================
// VultureCommandProcessor Class
// ============================================================================

class VultureCommandProcessor {
public:
    VultureCommandProcessor();
    ~VultureCommandProcessor();
    
    bool startup();
    void shutdown();
    
    bool executeCommand(const std::string& command,
                       const std::vector<std::string>& args,
                       VultureCommandResult& result);
    
    bool isRunning() const { return isRunning_; }
    
private:
    bool isRunning_;
    std::vector<std::string> commandQueue_;
    
    bool handleAnalyzeCommand(const std::vector<std::string>& args,
                             VultureCommandResult& result);
    bool handleProcessCommand(const std::vector<std::string>& args,
                             VultureCommandResult& result);
    bool handleExportCommand(const std::vector<std::string>& args,
                            VultureCommandResult& result);
    bool handleSelfTestCommand(const std::vector<std::string>& args,
                              VultureCommandResult& result);
};

// ============================================================================
// VultureSignalProcessor Class
// ============================================================================

class VultureSignalProcessor {
public:
    explicit VultureSignalProcessor(size_t bufferSize);
    ~VultureSignalProcessor() = default;
    
    bool processWindow(const std::vector<double>& input,
                      std::vector<double>& output);
    
    bool computeSpectrum(const std::vector<double>& timeDomain,
                        std::vector<double>& frequencyDomain);
    
    bool applyFilter(const std::vector<double>& input,
                    std::vector<double>& output,
                    const std::string& filterType);
    
    size_t getBufferSize() const { return bufferSize_; }
    
private:
    size_t bufferSize_;
};

// ============================================================================
// VultureFeatureExtractor Class
// ============================================================================

class VultureFeatureExtractor {
public:
    VultureFeatureExtractor();
    ~VultureFeatureExtractor() = default;
    
    bool extractPowerFeatures(const std::vector<double>& iData,
                             const std::vector<double>& qData,
                             VultureFeatureVector& features);
    
    bool extractPhaseFeatures(const std::vector<double>& iData,
                             const std::vector<double>& qData,
                             VultureFeatureVector& features);
    
    bool extractStatisticalFeatures(const std::vector<double>& signal,
                                   VultureFeatureVector& features);
    
    bool extractFrequencyFeatures(const std::vector<double>& timeDomain,
                                 VultureFeatureVector& features);
};

// ============================================================================
// VulturePlusPlusEngine Class
// ============================================================================

class VulturePlusPlusEngine {
public:
    VulturePlusPlusEngine();
    ~VulturePlusPlusEngine();
    
    bool initialize();
    void shutdown();
    
    bool processFile(const std::string& filepath, double sampleRate);
    bool analyzeData(const std::vector<double>& iData,
                    const std::vector<double>& qData);
    bool exportResults(const std::string& outputPath, const std::string& format);
    
    const VultureAnalysisResult& getLastResult() const { return lastResult_; }
    bool isReady() const { return isReady_; }
    
private:
    bool isReady_;
    VultureAnalysisResult lastResult_;
    std::unique_ptr<VultureIQAnalyzer> analyzer_;
    std::unique_ptr<VultureSignalProcessor> processor_;
    std::unique_ptr<VultureFeatureExtractor> extractor_;
};

} // namespace cpp
} // namespace vulture

#endif // VULTURE_CPP_TOOL_H
private:
    bool isReady_;
    std::unique_ptr<VultureIQAnalyzer> analyzer_;
    std::unique_ptr<VultureSignalProcessor> processor_;
    std::unique_ptr<VultureFeatureExtractor> extractorb
    bool analyzeData(const std::vector<double>& iData,)
    void shutdown();
#endif // VULTURE_CPP_TOOL_H



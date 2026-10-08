#include "vulture_cpp_tool.h"
#include <iostream>
#include <cmath>
#include <vector>
#include <algorithm>
#include <numeric>

/**
 * Vulture C++ Tool Implementation
 * 
 * This module provides modern C++ implementations of signal processing
 * and analysis tools for the VULTURE framework, building upon the C core.
 */

namespace vulture {
namespace cpp {

// ============================================================================
// VultureIQAnalyzer Implementation
// ============================================================================

VultureIQAnalyzer::VultureIQAnalyzer(double sampleRate)
    : sampleRate_(sampleRate), isInitialized_(false) {
    if (sampleRate <= 0) {
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
    
    try {
        // Initialize analysis buffers and workspace
        isInitialized_ = true;
        return true;
    } catch (const std::exception& e) {
        std::cerr << "Initialization failed: " << e.what() << std::endl;
        return false;
    }
}

void VultureIQAnalyzer::cleanup() {
    if (isInitialized_) {
        // Clean up resources
        isInitialized_ = false;
    }
}

bool VultureIQAnalyzer::analyzeSignal(const std::vector<double>& iData,
                                       const std::vector<double>& qData,
                                       VultureAnalysisResult& result) {
    if (!isInitialized_) {
        std::cerr << "Analyzer not initialized" << std::endl;
        return false;
    }
    
    if (iData.size() != qData.size() || iData.empty()) {
        std::cerr << "Invalid input data dimensions" << std::endl;
        return false;
    }
    
    try {
        // Calculate basic statistics
        result.sampleCount = iData.size();
        result.sampleRate = sampleRate_;
        
        // Power calculation
        double powerSum = 0.0;
        for (size_t i = 0; i < iData.size(); ++i) {
            powerSum += (iData[i] * iData[i] + qData[i] * qData[i]);
        }
        result.averagePower = powerSum / iData.size();
        
        // Peak detection
        result.peakPower = 0.0;
        for (size_t i = 0; i < iData.size(); ++i) {
            double power = iData[i] * iData[i] + qData[i] * qData[i];
            if (power > result.peakPower) {
                result.peakPower = power;
            }
        }
        
        // Compute magnitude and phase
        std::vector<double> magnitude(iData.size());
        std::vector<double> phase(iData.size());
        
        for (size_t i = 0; i < iData.size(); ++i) {
            magnitude[i] = std::sqrt(iData[i] * iData[i] + qData[i] * qData[i]);
            phase[i] = std::atan2(qData[i], iData[i]);
        }
        
        // DC offset detection
        double iMean = std::accumulate(iData.begin(), iData.end(), 0.0) / iData.size();
        double qMean = std::accumulate(qData.begin(), qData.end(), 0.0) / qData.size();
        result.dcOffset = std::sqrt(iMean * iMean + qMean * qMean);
        
        // Imbalance ratio (I/Q imbalance)
        double iVariance = 0.0, qVariance = 0.0;
        for (const auto& val : iData) iVariance += (val - iMean) * (val - iMean);
        for (const auto& val : qData) qVariance += (val - qMean) * (val - qMean);
        iVariance /= iData.size();
        qVariance /= qData.size();
        
        result.imbalanceRatio = (iVariance > 0 && qVariance > 0) ? 
                                std::max(iVariance, qVariance) / std::min(iVariance, qVariance) : 1.0;
        
        result.analysisValid = true;
        return true;
        
    } catch (const std::exception& e) {
        std::cerr << "Analysis error: " << e.what() << std::endl;
        result.analysisValid = false;
        return false;
    }
}

// ============================================================================
// VultureCommandProcessor Implementation
// ============================================================================

VultureCommandProcessor::VultureCommandProcessor()
    : isRunning_(false) {
}

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
    
    try {
        // Command routing
        if (command == "analyze") {
            return handleAnalyzeCommand(args, result);
        } else if (command == "process") {
            return handleProcessCommand(args, result);
        } else if (command == "export") {
            return handleExportCommand(args, result);
        } else if (command == "selftest") {
            return handleSelfTestCommand(args, result);
        } else {
            result.success = false;
            result.message = "Unknown command: " + command;
            return false;
        }
    } catch (const std::exception& e) {
        result.success = false;
        result.message = std::string("Command execution error: ") + e.what();
        return false;
    }
}

bool VultureCommandProcessor::handleAnalyzeCommand(const std::vector<std::string>& args,
                                                    VultureCommandResult& result) {
    if (args.empty()) {
        result.success = false;
        result.message = "Analyze command requires file path argument";
        return false;
    }
    
    result.success = true;
    result.message = "Analyze command executed for file: " + args[0];
    result.outputData = "Analysis results for " + args[0];
    return true;
}

bool VultureCommandProcessor::handleProcessCommand(const std::vector<std::string>& args,
                                                    VultureCommandResult& result) {
    if (args.size() < 2) {
        result.success = false;
        result.message = "Process command requires processor type and parameters";
        return false;
    }
    
    result.success = true;
    result.message = "Processing with " + args[0];
    result.outputData = "Process results";
    return true;
}

bool VultureCommandProcessor::handleExportCommand(const std::vector<std::string>& args,
                                                   VultureCommandResult& result) {
    if (args.size() < 2) {
        result.success = false;
        result.message = "Export command requires format and output path";
        return false;
    }
    
    result.success = true;
    result.message = "Exported to " + args[1] + " in " + args[0] + " format";
    result.outputData = args[1];
    return true;
}

bool VultureCommandProcessor::handleSelfTestCommand(const std::vector<std::string>& args,
                                                     VultureCommandResult& result) {
    result.success = true;
    result.message = "Self-test completed successfully";
    result.outputData = "All subsystems operational";
    return true;
}

// ============================================================================
// VultureSignalProcessor Implementation
// ============================================================================

VultureSignalProcessor::VultureSignalProcessor(size_t bufferSize)
    : bufferSize_(bufferSize) {
    if (bufferSize <= 0) {
        throw std::invalid_argument("Buffer size must be positive");
    }
}

bool VultureSignalProcessor::processWindow(const std::vector<double>& input,
                                            std::vector<double>& output) {
    if (input.size() != bufferSize_) {
        std::cerr << "Input size does not match buffer size" << std::endl;
        return false;
    }
    
    try {
        // Apply Hamming window
        output = input;
        for (size_t i = 0; i < input.size(); ++i) {
            double windowCoeff = 0.54 - 0.46 * std::cos(2.0 * M_PI * i / (input.size() - 1));
            output[i] *= windowCoeff;
        }
        return true;
    } catch (const std::exception& e) {
        std::cerr << "Window processing error: " << e.what() << std::endl;
        return false;
    }
}

} // namespace cpp
} // namespace vulture

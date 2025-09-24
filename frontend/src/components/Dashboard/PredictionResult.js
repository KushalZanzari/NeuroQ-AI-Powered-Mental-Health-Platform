import React from 'react';
import { 
  CheckCircleIcon, 
  ExclamationTriangleIcon,
  InformationCircleIcon,
  HeartIcon
} from '@heroicons/react/24/outline';

const PredictionResult = ({ prediction }) => {
  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'severe':
        return 'text-red-600 bg-red-100 dark:bg-red-900/20';
      case 'moderate':
        return 'text-yellow-600 bg-yellow-100 dark:bg-yellow-900/20';
      case 'mild':
        return 'text-green-600 bg-green-100 dark:bg-green-900/20';
      default:
        return 'text-blue-600 bg-blue-100 dark:bg-blue-900/20';
    }
  };

  const getConfidenceColor = (confidence) => {
    if (confidence >= 0.8) return 'text-green-600';
    if (confidence >= 0.6) return 'text-yellow-600';
    return 'text-red-600';
  };

  return (
    <div className="card">
      <div className="card-header">
        <div className="flex items-center">
          <HeartIcon className="h-6 w-6 text-primary-600 mr-2" />
          <h3 className="card-title">Analysis Results</h3>
        </div>
      </div>
      <div className="card-content space-y-4">
        {/* Disorder Prediction */}
        <div className="flex items-center justify-between p-4 bg-accent rounded-lg">
          <div>
            <h4 className="font-medium text-foreground">Predicted Condition</h4>
            <p className="text-lg font-semibold text-foreground">
              {prediction.predicted_disorder}
            </p>
          </div>
          <div className="text-right">
            <p className="text-sm text-muted-foreground">Confidence</p>
            <p className={`text-lg font-semibold ${getConfidenceColor(prediction.confidence_score)}`}>
              {Math.round(prediction.confidence_score * 100)}%
            </p>
          </div>
        </div>

        {/* Severity Level */}
        <div className="flex items-center space-x-2">
          <span className="text-sm font-medium text-foreground">Severity:</span>
          <span className={`px-2 py-1 rounded-full text-xs font-medium ${getSeverityColor(prediction.severity_level)}`}>
            {prediction.severity_level.charAt(0).toUpperCase() + prediction.severity_level.slice(1)}
          </span>
        </div>

        {/* Emergency Warning */}
        {prediction.emergency_contact_suggested && (
          <div className="flex items-start p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
            <ExclamationTriangleIcon className="h-5 w-5 text-red-600 mr-2 mt-0.5" />
            <div>
              <p className="text-sm font-medium text-red-800 dark:text-red-200">
                Immediate Support Recommended
              </p>
              <p className="text-xs text-red-700 dark:text-red-300 mt-1">
                Please consider reaching out to a mental health professional or crisis support immediately.
              </p>
            </div>
          </div>
        )}

        {/* Recommendations */}
        <div>
          <h4 className="font-medium text-foreground mb-2 flex items-center">
            <InformationCircleIcon className="h-4 w-4 mr-1" />
            Recommendations
          </h4>
          <p className="text-sm text-muted-foreground leading-relaxed">
            {prediction.recommendations}
          </p>
        </div>

        {/* Next Steps */}
        <div>
          <h4 className="font-medium text-foreground mb-2 flex items-center">
            <CheckCircleIcon className="h-4 w-4 mr-1" />
            Next Steps
          </h4>
          <div className="text-sm text-muted-foreground">
            {prediction.next_steps.split('\n').map((step, index) => (
              <p key={index} className="mb-1">
                {step}
              </p>
            ))}
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex space-x-2 pt-4 border-t border-border">
          <button className="btn btn-primary flex-1">
            Start AI Chat
          </button>
          <button className="btn btn-outline flex-1">
            Save Results
          </button>
        </div>
      </div>
    </div>
  );
};

export default PredictionResult;

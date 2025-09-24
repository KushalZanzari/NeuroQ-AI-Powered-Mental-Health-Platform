import React from 'react';
import { ClockIcon, EyeIcon } from '@heroicons/react/24/outline';

const RecentSubmissions = () => {
  // Mock data - in real app, this would come from API
  const submissions = [
    {
      id: 1,
      date: '2 hours ago',
      disorder: 'Anxiety',
      severity: 'moderate',
      confidence: 0.75,
    },
    {
      id: 2,
      date: '1 day ago',
      disorder: 'Depression',
      severity: 'mild',
      confidence: 0.68,
    },
    {
      id: 3,
      date: '3 days ago',
      disorder: 'No Disorder',
      severity: 'mild',
      confidence: 0.82,
    },
  ];

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

  return (
    <div className="card">
      <div className="card-header">
        <h3 className="card-title">Recent Submissions</h3>
        <p className="card-description">Your latest mental health check-ins</p>
      </div>
      <div className="card-content">
        <div className="space-y-3">
          {submissions.map((submission) => (
            <div
              key={submission.id}
              className="flex items-center justify-between p-3 border border-border rounded-lg hover:bg-accent transition-colors"
            >
              <div className="flex items-center space-x-3">
                <div className="flex items-center text-muted-foreground">
                  <ClockIcon className="h-4 w-4 mr-1" />
                  <span className="text-sm">{submission.date}</span>
                </div>
                <div>
                  <p className="font-medium text-foreground">
                    {submission.disorder}
                  </p>
                  <div className="flex items-center space-x-2">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${getSeverityColor(submission.severity)}`}>
                      {submission.severity}
                    </span>
                    <span className="text-xs text-muted-foreground">
                      {Math.round(submission.confidence * 100)}% confidence
                    </span>
                  </div>
                </div>
              </div>
              <button className="p-1 text-muted-foreground hover:text-foreground">
                <EyeIcon className="h-4 w-4" />
              </button>
            </div>
          ))}
        </div>
        
        {submissions.length === 0 && (
          <div className="text-center py-6">
            <p className="text-muted-foreground">No submissions yet</p>
            <p className="text-sm text-muted-foreground mt-1">
              Complete your first mental health check-in above
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default RecentSubmissions;

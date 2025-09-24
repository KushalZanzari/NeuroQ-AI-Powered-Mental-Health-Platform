import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { useAuthStore } from '../../store/authStore';
import { 
  HeartIcon, 
  ChartBarIcon,
  ChatBubbleLeftRightIcon,
  ExclamationTriangleIcon
} from '@heroicons/react/24/outline';
import SymptomForm from '../../components/Dashboard/SymptomForm';
import PredictionResult from '../../components/Dashboard/PredictionResult';
import RecentSubmissions from '../../components/Dashboard/RecentSubmissions';
import QuickStats from '../../components/Dashboard/QuickStats';
import LoadingSpinner from '../../components/UI/LoadingSpinner'; 
import toast from 'react-hot-toast';

const Dashboard = () => {
  const { user, isLoading: authLoading } = useAuthStore();
  const [prediction, setPrediction] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSymptomSubmit = async (data) => {
    setIsLoading(true);
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // Mock prediction result
      const mockPrediction = {
        predicted_disorder: 'Anxiety',
        confidence_score: 0.75,
        severity_level: 'moderate',
        recommendations: 'Consider practicing mindfulness meditation and deep breathing exercises. Maintain a regular sleep schedule and consider speaking with a mental health professional.',
        next_steps: '1. Practice daily meditation\n2. Maintain regular sleep schedule\n3. Consider therapy\n4. Monitor symptoms',
        emergency_contact_suggested: false
      };
      
      setPrediction(mockPrediction);
      toast.success('Analysis completed successfully!');
    } catch (error) {
      toast.error('Failed to analyze symptoms. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };
  if (authLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <LoadingSpinner />
        <p className="ml-2 text-lg text-muted-foreground">Loading your dashboard...</p>
      </div>
    );
  }

  // Show message if user failed to load
  if (!user) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-lg text-red-600">Failed to load user info. Please login again.</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Welcome Section */}
      <div className="bg-gradient-to-r from-primary-500 to-primary-600 rounded-lg p-6 text-white">
        <div className="flex items-center">
          <HeartIcon className="h-8 w-8 mr-3" />
          <div>
            <h1 className="text-2xl font-bold">
              Welcome back, {user?.full_name || user?.username}!
            </h1>
            <p className="text-primary-100">
              How are you feeling today? Let's check in with your mental health.
            </p>
          </div>
        </div>
      </div>

      {/* Quick Stats */}
      <QuickStats />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Symptom Form */}
        <div className="space-y-6">
          <div className="card">
            <div className="card-header">
              <div className="flex items-center">
                <ChartBarIcon className="h-6 w-6 text-primary-600 mr-2" />
                <h2 className="card-title">Mental Health Check-in</h2>
              </div>
              <p className="card-description">
                Share how you're feeling and get personalized insights
              </p>
            </div>
            <div className="card-content">
              <SymptomForm onSubmit={handleSymptomSubmit} isLoading={isLoading} />
            </div>
          </div>

          {/* Recent Submissions */}
          <RecentSubmissions />
        </div>

        {/* Results and Chat */}
        <div className="space-y-6">
          {prediction && (
            <PredictionResult prediction={prediction} />
          )}

          {/* Quick Actions */}
          <div className="card">
            <div className="card-header">
              <h3 className="card-title">Quick Actions</h3>
            </div>
            <div className="card-content space-y-4">
              <button className="w-full btn btn-outline flex items-center justify-center p-4 hover:bg-accent">
                <ChatBubbleLeftRightIcon className="h-5 w-5 mr-2" />
                Start AI Chat Session
              </button>
              
              <button className="w-full btn btn-outline flex items-center justify-center p-4 hover:bg-accent">
                <ChartBarIcon className="h-5 w-5 mr-2" />
                View Progress Reports
              </button>
              
              <button className="w-full btn btn-outline flex items-center justify-center p-4 hover:bg-accent">
                <HeartIcon className="h-5 w-5 mr-2" />
                Emergency Resources
              </button>
            </div>
          </div>

          {/* Emergency Notice */}
          <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4">
            <div className="flex items-start">
              <ExclamationTriangleIcon className="h-5 w-5 text-red-600 mr-2 mt-0.5" />
              <div>
                <h4 className="text-sm font-medium text-red-800 dark:text-red-200">
                  Crisis Support
                </h4>
                <p className="text-sm text-red-700 dark:text-red-300 mt-1">
                  If you're having thoughts of self-harm, please contact emergency services immediately or call a crisis hotline.
                </p>
                <p className="text-xs text-red-600 dark:text-red-400 mt-2">
                  National Suicide Prevention Lifeline: 988
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

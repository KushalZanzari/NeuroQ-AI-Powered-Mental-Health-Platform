import React from 'react';
import { 
  ChartBarIcon, 
  HeartIcon, 
  ChatBubbleLeftRightIcon,
  ClockIcon
} from '@heroicons/react/24/outline';

const QuickStats = () => {
  // Mock data - in real app, this would come from API
  const stats = [
    {
      title: 'Total Check-ins',
      value: '12',
      change: '+2 this week',
      icon: ChartBarIcon,
      color: 'text-blue-600',
      bgColor: 'bg-blue-100 dark:bg-blue-900/20',
    },
    {
      title: 'Current Streak',
      value: '5 days',
      change: 'Keep it up!',
      icon: HeartIcon,
      color: 'text-green-600',
      bgColor: 'bg-green-100 dark:bg-green-900/20',
    },
    {
      title: 'AI Sessions',
      value: '8',
      change: '+1 today',
      icon: ChatBubbleLeftRightIcon,
      color: 'text-purple-600',
      bgColor: 'bg-purple-100 dark:bg-purple-900/20',
    },
    {
      title: 'Last Check-in',
      value: '2 hours ago',
      change: 'Good timing',
      icon: ClockIcon,
      color: 'text-orange-600',
      bgColor: 'bg-orange-100 dark:bg-orange-900/20',
    },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      {stats.map((stat, index) => (
        <div key={index} className="card">
          <div className="card-content">
            <div className="flex items-center">
              <div className={`p-2 rounded-lg ${stat.bgColor}`}>
                <stat.icon className={`h-5 w-5 ${stat.color}`} />
              </div>
              <div className="ml-4 flex-1">
                <p className="text-sm font-medium text-muted-foreground">
                  {stat.title}
                </p>
                <p className="text-2xl font-bold text-foreground">
                  {stat.value}
                </p>
                <p className="text-xs text-muted-foreground">
                  {stat.change}
                </p>
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default QuickStats;

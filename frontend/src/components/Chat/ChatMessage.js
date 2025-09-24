import React from 'react';
import { UserIcon, HeartIcon } from '@heroicons/react/24/outline';

const ChatMessage = ({ message }) => {
  const isUser = message.is_user_message;
  const timestamp = new Date(message.created_at).toLocaleTimeString([], { 
    hour: '2-digit', 
    minute: '2-digit' 
  });

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div className={`flex max-w-[80%] ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
        {/* Avatar */}
        <div className={`flex-shrink-0 ${isUser ? 'ml-3' : 'mr-3'}`}>
          <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
            isUser 
              ? 'bg-primary-600 text-white' 
              : 'bg-accent text-primary-600'
          }`}>
            {isUser ? (
              <UserIcon className="h-5 w-5" />
            ) : (
              <HeartIcon className="h-5 w-5" />
            )}
          </div>
        </div>

        {/* Message Content */}
        <div className={`flex flex-col ${isUser ? 'items-end' : 'items-start'}`}>
          <div className={`px-4 py-2 rounded-lg ${
            isUser
              ? 'bg-primary-600 text-white rounded-br-sm'
              : 'bg-card border border-border text-foreground rounded-bl-sm'
          }`}>
            <p className="text-sm whitespace-pre-wrap">{message.message}</p>
          </div>
          
          {/* Timestamp and AI Model */}
          <div className={`flex items-center space-x-1 mt-1 text-xs text-muted-foreground ${
            isUser ? 'flex-row-reverse' : 'flex-row'
          }`}>
            <span>{timestamp}</span>
            {!isUser && message.ai_model_used && (
              <>
                <span>•</span>
                <span>{message.ai_model_used}</span>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatMessage;

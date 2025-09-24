import React, { useState, useEffect, useRef } from 'react';
import { useAuthStore } from '../../store/authStore';
import ChatMessage from '../../components/Chat/ChatMessage';
import ChatInput from '../../components/Chat/ChatInput';
import ChatHeader from '../../components/Chat/ChatHeader';
import { HeartIcon } from '@heroicons/react/24/outline';

const Chat = () => {
  const { user } = useAuthStore();
  const [messages, setMessages] = useState([]);
  const [isTyping, setIsTyping] = useState(false);
  const [currentSession, setCurrentSession] = useState(null);
  const messagesEndRef = useRef(null);

  // Mock initial messages
  useEffect(() => {
    const initialMessages = [
      {
        id: 1,
        message: "Hello! I'm your AI mental health companion. How are you feeling today?",
        response: "Hello! I'm your AI mental health companion. How are you feeling today?",
        is_user_message: false,
        created_at: new Date().toISOString(),
        ai_model_used: "NeuroQ AI"
      }
    ];
    setMessages(initialMessages);
  }, []);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (message) => {
    // Add user message
    const userMessage = {
      id: Date.now(),
      message,
      is_user_message: true,
      created_at: new Date().toISOString(),
    };
    
    setMessages(prev => [...prev, userMessage]);
    setIsTyping(true);

    // Simulate AI response
    setTimeout(() => {
      const aiResponse = generateAIResponse(message);
      const aiMessage = {
        id: Date.now() + 1,
        message: aiResponse,
        response: aiResponse,
        is_user_message: false,
        created_at: new Date().toISOString(),
        ai_model_used: "NeuroQ AI"
      };
      
      setMessages(prev => [...prev, aiMessage]);
      setIsTyping(false);
    }, 1500);
  };

  const generateAIResponse = (userMessage) => {
    const message = userMessage.toLowerCase();
    
    if (message.includes('anxiety') || message.includes('anxious')) {
      return "I understand you're feeling anxious. That's completely normal. Can you tell me more about what's making you feel this way? Sometimes talking about it can help.";
    } else if (message.includes('depressed') || message.includes('sad')) {
      return "I'm sorry you're feeling this way. It takes courage to share these feelings. Have you been able to maintain your daily routines? Sometimes small steps can make a big difference.";
    } else if (message.includes('sleep') || message.includes('tired')) {
      return "Sleep issues can really impact how we feel. What's your current sleep schedule like? I might have some suggestions that could help.";
    } else if (message.includes('help') || message.includes('support')) {
      return "I'm here to help and support you. What specific area would you like to work on? Whether it's managing stress, improving mood, or building better habits, we can tackle it together.";
    } else if (message.includes('thank')) {
      return "You're very welcome! I'm here whenever you need to talk. Remember, taking care of your mental health is important, and you're doing great by reaching out.";
    } else {
      return "Thank you for sharing that with me. I'm here to listen and help. Can you tell me more about what's on your mind today?";
    }
  };

  const startNewSession = () => {
    setCurrentSession({
      id: Date.now(),
      name: `Chat ${new Date().toLocaleDateString()}`,
      created_at: new Date().toISOString()
    });
    setMessages([]);
  };

  return (
    <div className="h-[calc(100vh-8rem)] flex flex-col">
      {/* Chat Header */}
      <ChatHeader 
        currentSession={currentSession}
        onNewSession={startNewSession}
      />

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-center">
            <HeartIcon className="h-16 w-16 text-primary-200 mb-4" />
            <h3 className="text-lg font-medium text-foreground mb-2">
              Welcome to AI Chat
            </h3>
            <p className="text-muted-foreground mb-6 max-w-md">
              I'm here to help you with your mental health journey. Start a conversation by typing a message below.
            </p>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 max-w-2xl">
              <button
                onClick={() => handleSendMessage("I'm feeling anxious today")}
                className="p-4 text-left border border-border rounded-lg hover:bg-accent transition-colors"
              >
                <h4 className="font-medium text-foreground mb-1">Feeling Anxious</h4>
                <p className="text-sm text-muted-foreground">I'm feeling anxious today</p>
              </button>
              <button
                onClick={() => handleSendMessage("I'm having trouble sleeping")}
                className="p-4 text-left border border-border rounded-lg hover:bg-accent transition-colors"
              >
                <h4 className="font-medium text-foreground mb-1">Sleep Issues</h4>
                <p className="text-sm text-muted-foreground">I'm having trouble sleeping</p>
              </button>
              <button
                onClick={() => handleSendMessage("I need help with my mood")}
                className="p-4 text-left border border-border rounded-lg hover:bg-accent transition-colors"
              >
                <h4 className="font-medium text-foreground mb-1">Mood Support</h4>
                <p className="text-sm text-muted-foreground">I need help with my mood</p>
              </button>
              <button
                onClick={() => handleSendMessage("I want to talk about stress")}
                className="p-4 text-left border border-border rounded-lg hover:bg-accent transition-colors"
              >
                <h4 className="font-medium text-foreground mb-1">Stress Management</h4>
                <p className="text-sm text-muted-foreground">I want to talk about stress</p>
              </button>
            </div>
          </div>
        ) : (
          <>
            {messages.map((message) => (
              <ChatMessage key={message.id} message={message} />
            ))}
            {isTyping && (
              <div className="flex items-center space-x-2 text-muted-foreground">
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-primary-600 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-primary-600 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                  <div className="w-2 h-2 bg-primary-600 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                </div>
                <span className="text-sm">AI is typing...</span>
              </div>
            )}
            <div ref={messagesEndRef} />
          </>
        )}
      </div>

      {/* Chat Input */}
      <div className="border-t border-border p-4">
        <ChatInput onSendMessage={handleSendMessage} disabled={isTyping} />
      </div>
    </div>
  );
};

export default Chat;

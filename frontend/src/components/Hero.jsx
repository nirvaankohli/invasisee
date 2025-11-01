import React from 'react';
import { Button } from './Button';

export const Hero = () => {
  return (
    <section className="relative pt-24 pb-20 sm:pt-32 sm:pb-28 overflow-hidden">
      {/* Organic blob background */}
      <div className="absolute inset-0 -z-10 overflow-hidden">
        <div className="absolute top-20 right-0 w-96 h-96 bg-gradient-to-br from-green-200/40 to-green-300/40 rounded-full blur-3xl opacity-60 animate-pulse" 
             style={{ animationDuration: '4s' }} 
             aria-hidden="true" />
        <div className="absolute bottom-0 left-0 w-80 h-80 bg-gradient-to-tr from-green-100/50 to-green-200/50 rounded-full blur-3xl opacity-50 animate-pulse" 
             style={{ animationDuration: '5s', animationDelay: '1s' }} 
             aria-hidden="true" />
      </div>

      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          {/* Left column: Text content */}
          <div className="text-center lg:text-left space-y-8 animate-fade-in">
            <h1 className="text-6xl sm:text-7xl lg:text-8xl font-display font-bold text-gray-900 leading-tight text-balance">
              Spot. Verify. Protect.
            </h1>
            
            <p className="text-xl sm:text-2xl text-gray-600 max-w-2xl mx-auto lg:mx-0 text-balance font-serif font-light leading-relaxed">
              Join our community in protecting local ecosystems by identifying and reporting invasive species.
            </p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start pt-4">
              <Button 
                variant="primary" 
                href="#map"
                ariaLabel="Explore the invasive species map"
                className="text-lg"
              >
                Explore Map
              </Button>
              <Button 
                variant="outline" 
                href="#how-it-works"
                ariaLabel="Learn how InvaSee works"
                className="text-lg"
              >
                How It Works
              </Button>
            </div>
          </div>

          {/* Right column: Phone mock */}
          <div className="relative flex justify-center lg:justify-end animate-fade-in" style={{ animationDelay: '0.2s' }}>
            {/* Gradient backdrop */}
            <div className="absolute inset-0 flex items-center justify-center lg:justify-end">
              <div className="w-80 h-80 sm:w-96 sm:h-96 bg-gradient-to-br from-green-400 to-green-600 rounded-full opacity-20 blur-2xl" 
                   aria-hidden="true" />
            </div>
            
            {/* Phone mock */}
            <div className="relative z-10 w-72 sm:w-80 bg-white rounded-3xl shadow-2xl p-2 border-8 border-gray-800 transition-transform hover:scale-105 duration-300">
              <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-2xl aspect-[9/19] flex flex-col items-center justify-center p-6 space-y-4">
                {/* App preview placeholder */}
                <div className="w-full h-24 bg-white rounded-xl shadow-sm flex items-center justify-center">
                  <svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                    <path d="M24 4C20 4 16 6 13 9C10 12 8 16 8 20C8 24 10 28 13 31C16 34 20 36 24 36C28 36 32 34 35 31C38 28 40 24 40 20C40 16 38 12 35 9C32 6 28 4 24 4Z" fill="url(#phoneGradient)"/>
                    <path d="M24 12C21 12 18 13.5 16.5 15.5C15 17.5 14 20 14 23C14 26 15 28.5 16.5 30.5C18 32.5 21 34 24 34C27 34 30 32.5 31.5 30.5C33 28.5 34 26 34 23C34 20 33 17.5 31.5 15.5C30 13.5 27 12 24 12Z" fill="white" opacity="0.4"/>
                    <defs>
                      <linearGradient id="phoneGradient" x1="8" y1="4" x2="40" y2="36">
                        <stop offset="0%" stopColor="#22c55e"/>
                        <stop offset="100%" stopColor="#16a34a"/>
                      </linearGradient>
                    </defs>
                  </svg>
                </div>
                
                <div className="w-full space-y-2">
                  <div className="h-4 bg-white rounded shadow-sm w-3/4 mx-auto" aria-hidden="true" />
                  <div className="h-4 bg-white rounded shadow-sm w-1/2 mx-auto" aria-hidden="true" />
                </div>
                
                <div className="w-full h-32 bg-white rounded-xl shadow-sm" aria-hidden="true" />
                
                <div className="flex space-x-2 pt-2">
                  <div className="w-12 h-12 bg-green-500 rounded-full shadow-md" aria-hidden="true" />
                  <div className="w-12 h-12 bg-green-400 rounded-full shadow-md" aria-hidden="true" />
                  <div className="w-12 h-12 bg-green-300 rounded-full shadow-md" aria-hidden="true" />
                </div>
              </div>
            </div>

            {/* Decorative leaves */}
            <svg 
              className="absolute -top-8 -left-8 w-24 h-24 text-green-500 opacity-30 animate-float" 
              viewBox="0 0 100 100" 
              fill="currentColor"
              aria-hidden="true"
            >
              <path d="M50 10C30 10 15 25 10 40C5 55 10 75 25 85C40 95 60 95 75 85C90 75 95 55 90 40C85 25 70 10 50 10Z" />
            </svg>
            
            <svg 
              className="absolute -bottom-8 -right-8 w-32 h-32 text-green-400 opacity-20 animate-float" 
              style={{ animationDelay: '1s' }}
              viewBox="0 0 100 100" 
              fill="currentColor"
              aria-hidden="true"
            >
              <path d="M50 5C25 5 10 20 5 35C0 50 5 70 20 85C35 100 65 100 80 85C95 70 100 50 95 35C90 20 75 5 50 5Z" />
            </svg>
          </div>
        </div>
      </div>
    </section>
  );
};

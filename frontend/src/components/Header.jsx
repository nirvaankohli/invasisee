import React from 'react';
import { Button } from './Button';

export const Header = () => {
  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-white/90 backdrop-blur-sm border-b border-gray-100">
      <nav className="container mx-auto px-4 sm:px-6 lg:px-8 py-4" aria-label="Main navigation">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <div className="flex items-center space-x-2">
            <svg 
              width="32" 
              height="32" 
              viewBox="0 0 32 32" 
              fill="none" 
              xmlns="http://www.w3.org/2000/svg"
              aria-hidden="true"
            >
              <path 
                d="M16 4C13 4 10 6 8 8C6 10 4 13 4 16C4 19 6 22 8 24C10 26 13 28 16 28C19 28 22 26 24 24C26 22 28 19 28 16C28 13 26 10 24 8C22 6 19 4 16 4Z" 
                fill="url(#leafGradient)"
              />
              <path 
                d="M16 8C14 8 12 9 11 10C10 11 9 13 9 15C9 17 10 19 11 20C12 21 14 22 16 22C18 22 20 21 21 20C22 19 23 17 23 15C23 13 22 11 21 10C20 9 18 8 16 8Z" 
                fill="white" 
                opacity="0.3"
              />
              <defs>
                <linearGradient id="leafGradient" x1="4" y1="4" x2="28" y2="28">
                  <stop offset="0%" stopColor="#22c55e" />
                  <stop offset="100%" stopColor="#16a34a" />
                </linearGradient>
              </defs>
            </svg>
            <span className="text-xl font-serif font-semibold text-gray-900">InvaSee</span>
          </div>

          {/* Navigation Links */}
          <div className="flex items-center space-x-4">
            <a 
              href="#map" 
              className="text-gray-700 hover:text-green-600 font-medium transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 rounded px-2 py-1"
              aria-label="Go to map section"
            >
              Map
            </a>
            <Button variant="primary" href="#report" ariaLabel="Start reporting invasive species">
              Start Reporting
            </Button>
          </div>
        </div>
      </nav>
    </header>
  );
};

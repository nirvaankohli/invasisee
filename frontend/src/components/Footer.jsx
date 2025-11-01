import React from 'react';

export const Footer = () => {
  return (
    <footer className="bg-gray-900 text-white py-12" role="contentinfo">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid md:grid-cols-3 gap-8 mb-8">
          {/* Brand */}
          <div className="space-y-4">
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
                  fill="url(#footerGradient)"
                />
                <defs>
                  <linearGradient id="footerGradient" x1="4" y1="4" x2="28" y2="28">
                    <stop offset="0%" stopColor="#22c55e" />
                    <stop offset="100%" stopColor="#16a34a" />
                  </linearGradient>
                </defs>
              </svg>
              <span className="text-xl font-bold">InvaSee</span>
            </div>
            <p className="text-gray-400 text-sm">
              Protecting our ecosystems together, one report at a time.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="font-bold mb-4">Quick Links</h3>
            <ul className="space-y-2">
              <li>
                <a 
                  href="#how-it-works" 
                  className="text-gray-400 hover:text-green-400 transition-colors focus:outline-none focus:ring-2 focus:ring-green-400 focus:ring-offset-2 focus:ring-offset-gray-900 rounded"
                  aria-label="Learn how InvaSee works"
                >
                  How It Works
                </a>
              </li>
              <li>
                <a 
                  href="#map" 
                  className="text-gray-400 hover:text-green-400 transition-colors focus:outline-none focus:ring-2 focus:ring-green-400 focus:ring-offset-2 focus:ring-offset-gray-900 rounded"
                  aria-label="Explore the map"
                >
                  Map
                </a>
              </li>
              <li>
                <a 
                  href="#report" 
                  className="text-gray-400 hover:text-green-400 transition-colors focus:outline-none focus:ring-2 focus:ring-green-400 focus:ring-offset-2 focus:ring-offset-gray-900 rounded"
                  aria-label="Start reporting"
                >
                  Start Reporting
                </a>
              </li>
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h3 className="font-bold mb-4">Connect</h3>
            <ul className="space-y-2">
              <li>
                <a 
                  href="mailto:info@invasee.com" 
                  className="text-gray-400 hover:text-green-400 transition-colors focus:outline-none focus:ring-2 focus:ring-green-400 focus:ring-offset-2 focus:ring-offset-gray-900 rounded"
                  aria-label="Email us at info@invasee.com"
                >
                  info@invasee.com
                </a>
              </li>
              <li className="flex space-x-4 pt-2">
                <a 
                  href="#" 
                  className="text-gray-400 hover:text-green-400 transition-colors focus:outline-none focus:ring-2 focus:ring-green-400 focus:ring-offset-2 focus:ring-offset-gray-900 rounded p-1"
                  aria-label="Follow us on social media"
                >
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                    <path d="M12 2C6.477 2 2 6.477 2 12c0 4.991 3.657 9.128 8.438 9.879V14.89h-2.54V12h2.54V9.797c0-2.506 1.492-3.89 3.777-3.89 1.094 0 2.238.195 2.238.195v2.46h-1.26c-1.243 0-1.63.771-1.63 1.562V12h2.773l-.443 2.89h-2.33v6.989C18.343 21.129 22 16.99 22 12c0-5.523-4.477-10-10-10z"/>
                  </svg>
                </a>
              </li>
            </ul>
          </div>
        </div>

        <div className="border-t border-gray-800 pt-8 text-center text-gray-400 text-sm">
          <p>&copy; {new Date().getFullYear()} InvaSee. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
};

import React from 'react';

const StepCard = ({ icon, title, description, delay = 0 }) => (
  <div 
    className="bg-white rounded-2xl p-8 shadow-lg hover:shadow-xl transition-all duration-300 border border-gray-100 animate-fade-in group hover:-translate-y-1"
    style={{ animationDelay: `${delay}s` }}
  >
    <div className="flex flex-col items-center text-center space-y-4">
      <div className="w-16 h-16 bg-gradient-to-br from-green-400 to-green-600 rounded-2xl flex items-center justify-center shadow-md group-hover:scale-110 transition-transform duration-300">
        {icon}
      </div>
      <h3 className="text-xl font-bold text-gray-900">{title}</h3>
      <p className="text-gray-600 leading-relaxed">{description}</p>
    </div>
  </div>
);

export const HowItWorks = () => {
  return (
    <section id="how-it-works" className="py-20 sm:py-28 bg-gradient-to-b from-white to-green-50/30">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16 animate-fade-in">
          <h2 className="text-4xl sm:text-5xl font-bold text-gray-900 mb-4 text-balance">
            How It Works
          </h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto text-balance">
            Three simple steps to help protect our ecosystem
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
          <StepCard
            icon={
              <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                <path d="M16 4C15 4 14 4.5 13 5.5L4 14.5C3 15.5 3 17 4 18L14 28C15 29 16.5 29 17.5 28L27.5 18C28.5 17 28.5 15.5 27.5 14.5L18 5C17 4.5 17 4 16 4Z" fill="white"/>
                <circle cx="16" cy="16" r="4" fill="white"/>
              </svg>
            }
            title="Spot"
            description="Discover an invasive species in your area using our identification guide."
            delay={0}
          />

          <StepCard
            icon={
              <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                <path d="M16 2L20 12L30 14L22 22L24 32L16 27L8 32L10 22L2 14L12 12L16 2Z" fill="white"/>
              </svg>
            }
            title="Verify"
            description="Upload a photo and location to help our community confirm the sighting."
            delay={0.1}
          />

          <StepCard
            icon={
              <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                <path d="M16 4C13 4 10 6 8 8C6 10 4 13 4 16C4 19 6 22 8 24C10 26 13 28 16 28C19 28 22 26 24 24C26 22 28 19 28 16C28 13 26 10 24 8C22 6 19 4 16 4Z" fill="white"/>
                <path d="M12 16L15 19L21 13" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            }
            title="Protect"
            description="Contribute to local conservation efforts and watch your impact grow."
            delay={0.2}
          />
        </div>
      </div>
    </section>
  );
};

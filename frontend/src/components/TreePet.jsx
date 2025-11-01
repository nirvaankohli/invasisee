import React from 'react';

const GrowthStep = ({ stage, title, description, size, delay = 0 }) => (
  <div 
    className="flex flex-col items-center text-center space-y-4 animate-fade-in"
    style={{ animationDelay: `${delay}s` }}
  >
    <div className={`bg-gradient-to-br from-green-400 to-green-600 rounded-full ${size} flex items-center justify-center shadow-lg hover:scale-110 transition-transform duration-300`}>
      <svg 
        viewBox="0 0 100 100" 
        fill="white" 
        className="w-3/4 h-3/4"
        aria-hidden="true"
      >
        {stage === 1 && (
          <path d="M50 70C50 70 45 60 45 50C45 40 48 35 50 30C52 35 55 40 55 50C55 60 50 70 50 70Z" />
        )}
        {stage === 2 && (
          <g>
            <path d="M50 75C50 75 45 65 45 55C45 45 48 40 50 35C52 40 55 45 55 55C55 65 50 75 50 75Z" />
            <path d="M40 60C40 60 35 55 35 50C35 45 37 42 40 40C42 42 45 45 45 50C45 55 40 60 40 60Z" />
            <path d="M60 60C60 60 65 55 65 50C65 45 63 42 60 40C58 42 55 45 55 50C55 55 60 60 60 60Z" />
          </g>
        )}
        {stage === 3 && (
          <g>
            <path d="M50 80C50 80 45 70 45 60C45 50 48 45 50 40C52 45 55 50 55 60C55 70 50 80 50 80Z" />
            <path d="M35 65C35 65 30 60 30 55C30 50 32 47 35 45C37 47 40 50 40 55C40 60 35 65 35 65Z" />
            <path d="M65 65C65 65 70 60 70 55C70 50 68 47 65 45C63 47 60 50 60 55C60 60 65 65 65 65Z" />
            <path d="M42 72C42 72 38 68 38 64C38 60 40 58 42 56C44 58 46 60 46 64C46 68 42 72 42 72Z" />
            <path d="M58 72C58 72 62 68 62 64C62 60 60 58 58 56C56 58 54 60 54 64C54 68 58 72 58 72Z" />
          </g>
        )}
        {/* Trunk */}
        <rect x="47" y={stage === 1 ? "70" : stage === 2 ? "75" : "80"} width="6" height="15" fill="currentColor" />
      </svg>
    </div>
    <div>
      <h3 className="font-bold text-gray-900 mb-2">{title}</h3>
      <p className="text-sm text-gray-600">{description}</p>
    </div>
  </div>
);

export const TreePet = () => {
  return (
    <section className="py-20 sm:py-28 bg-gradient-to-b from-green-50/30 to-white">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto text-center animate-fade-in">
          <h2 className="text-5xl sm:text-6xl font-display font-bold text-gray-900 mb-4 text-balance">
            Watch Your Impact Grow
          </h2>
          <p className="text-xl text-gray-600 mb-16 max-w-2xl mx-auto text-balance font-serif font-light">
            Nurture your virtual tree pet as you contribute to protecting real ecosystems.
          </p>

          <div className="grid sm:grid-cols-3 gap-12 mb-12">
            <GrowthStep
              stage={1}
              title="Seedling"
              description="Start your journey with your first report"
              size="w-20 h-20"
              delay={0}
            />
            <GrowthStep
              stage={2}
              title="Sapling"
              description="Your tree grows as you make more contributions"
              size="w-24 h-24"
              delay={0.1}
            />
            <GrowthStep
              stage={3}
              title="Mighty Tree"
              description="Become a conservation champion with a full-grown tree"
              size="w-28 h-28"
              delay={0.2}
            />
          </div>

          <div className="bg-gradient-to-r from-green-50 to-green-100 rounded-2xl p-8 border border-green-200 shadow-lg">
            <p className="text-lg text-green-800 font-medium mb-4">
              🌱 Every report helps your tree grow and contributes to real-world conservation efforts
            </p>
            <p className="text-gray-700">
              Track your progress, compete with friends, and see the collective impact of our community.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
};

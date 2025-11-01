import React, { lazy, Suspense } from 'react';
import { Button } from './Button';

// Lazy load map component (placeholder for future implementation)
const MapPlaceholder = lazy(() => Promise.resolve({
  default: () => (
    <div className="w-full h-full bg-gradient-to-br from-green-100 to-green-200 rounded-xl flex items-center justify-center">
      <div className="text-center space-y-4">
        <svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg" className="mx-auto" aria-hidden="true">
          <path d="M32 8L8 20V52L32 40L56 52V20L32 8Z" fill="url(#mapGradient)" />
          <path d="M32 8V40M8 20L32 8L56 20M8 52L32 40L56 52" stroke="white" strokeWidth="2" strokeLinecap="round" />
          <defs>
            <linearGradient id="mapGradient" x1="8" y1="8" x2="56" y2="52">
              <stop offset="0%" stopColor="#22c55e" />
              <stop offset="100%" stopColor="#16a34a" />
            </linearGradient>
          </defs>
        </svg>
        <p className="text-green-700 font-medium">Interactive Map</p>
      </div>
    </div>
  )
}));

export const MapPreview = () => {
  return (
    <section id="map" className="py-20 sm:py-28 bg-white">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="max-w-5xl mx-auto">
          <div className="bg-gradient-to-br from-green-50 to-white rounded-3xl shadow-2xl overflow-hidden border border-green-100 animate-fade-in">
            <div className="p-8 sm:p-12">
              <div className="text-center mb-8">
                <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 mb-4 text-balance">
                  Explore the Map
                </h2>
                <p className="text-lg text-gray-600 max-w-2xl mx-auto text-balance">
                  See real-time invasive species sightings in your area and contribute to our growing database.
                </p>
              </div>

              {/* Map placeholder with lazy loading */}
              <div className="aspect-video w-full mb-8 rounded-xl overflow-hidden shadow-lg">
                <Suspense 
                  fallback={
                    <div className="w-full h-full bg-gray-100 flex items-center justify-center">
                      <div className="text-center">
                        <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-green-500 border-t-transparent" aria-label="Loading map"></div>
                        <p className="mt-4 text-gray-600">Loading map...</p>
                      </div>
                    </div>
                  }
                >
                  <MapPlaceholder />
                </Suspense>
              </div>

              <div className="flex justify-center">
                <Button 
                  variant="primary" 
                  href="#map"
                  ariaLabel="Explore the full interactive map"
                  className="text-lg"
                >
                  <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg" className="mr-2" aria-hidden="true">
                    <path d="M10 2L2 6V16L10 12L18 16V6L10 2Z" fill="currentColor" />
                    <path d="M10 2V12M2 6L10 2L18 6M2 16L10 12L18 16" stroke="white" strokeWidth="1.5" strokeLinecap="round" />
                  </svg>
                  Explore Map
                </Button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

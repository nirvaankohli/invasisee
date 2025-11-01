import React from 'react';
import { Header } from './components/Header';
import { Hero } from './components/Hero';
import { HowItWorks } from './components/HowItWorks';
import { MapPreview } from './components/MapPreview';
import { TreePet } from './components/TreePet';
import { Footer } from './components/Footer';

function App() {
  return (
    <div className="min-h-screen">
      <Header />
      <main>
        <Hero />
        <HowItWorks />
        <MapPreview />
        <TreePet />
      </main>
      <Footer />
    </div>
  );
}

export default App;

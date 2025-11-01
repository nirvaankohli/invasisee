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
      <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300..700;1,300..700&display=swap" rel="stylesheet"></link>
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

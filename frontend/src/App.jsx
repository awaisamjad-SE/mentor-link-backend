// File: src/App.jsx
import React from 'react';
import VehicleForm from './components/VehicleForm';
import InspectionForm from './components/InspectionForm';

export default function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 to-blue-700 text-white p-8">
      <div className="bg-white text-black rounded-xl p-6 max-w-5xl mx-auto shadow-lg space-y-8">
        <h1 className="text-3xl font-bold">Vehicle Inspection System</h1>
        <VehicleForm onCreated={(v) => alert(`Vehicle created with ID: ${v.id}`)} />
        <InspectionForm />
      </div>
    </div>
  );
}

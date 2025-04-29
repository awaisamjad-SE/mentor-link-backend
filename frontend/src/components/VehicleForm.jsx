// File: src/components/VehicleForm.jsx
import React, { useState } from 'react';
import { createVehicle } from '../api';

export default function VehicleForm({ onCreated }) {
  const [form, setForm] = useState({
    name: '',
    location: '',
    status: '',
    pending_work: '',
    exit_status: false
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setForm({
      ...form,
      [name]: type === 'checkbox' ? checked : value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const newVehicle = await createVehicle(form);
    onCreated(newVehicle);
    setForm({ name: '', location: '', status: '', pending_work: '', exit_status: false });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <input type="text" name="name" value={form.name} onChange={handleChange} placeholder="Vehicle Name" className="border p-2 w-full" required />
      <input type="text" name="location" value={form.location} onChange={handleChange} placeholder="Location" className="border p-2 w-full" required />
      <input type="text" name="status" value={form.status} onChange={handleChange} placeholder="Status" className="border p-2 w-full" required />
      <input type="text" name="pending_work" value={form.pending_work} onChange={handleChange} placeholder="Pending Work" className="border p-2 w-full" />
      <label className="flex items-center">
        <input type="checkbox" name="exit_status" checked={form.exit_status} onChange={handleChange} className="mr-2" /> Exit Status
      </label>
      <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded">Add Vehicle</button>
    </form>
  );
}

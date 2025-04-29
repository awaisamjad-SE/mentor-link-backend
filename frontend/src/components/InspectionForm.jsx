// File: src/components/InspectionForm.jsx
import React, { useState, useEffect } from 'react';
import { checkVehicle, getInspection, saveInspection } from '../api';

const presetParams = [
  "Top Ring Size", "Second Ring Gap", "Oil Ring Gap",
  "Valve Timing / Ignition Timing", "Crank Main and Small Bearing Torque",
  "Head Bolt Torque", "Crankshaft Bolt Torque", "Camshaft Bolt Torque",
  "Engine Leakage", "Abnormal Smoke, Abnormal Noise",
  "Engine Compression", "Engine Running (Hours)"
];

export default function InspectionForm() {
  const [vehicleId, setVehicleId] = useState('');
  const [params, setParams] = useState([]);

  const handleCheck = async () => {
    if (!vehicleId) return alert('Enter vehicle ID');
    const data = await checkVehicle(vehicleId);
    if (!data.exists) return alert('Vehicle does not exist. Please create it first.');
    const report = await getInspection(vehicleId, 'assembly');
    if (report.reports.length > 0) {
      setParams(report.reports);
    } else {
      setParams(presetParams.map(p => ({ parameter: p, status: 'pass', observation: '' })));
    }
  };

  const handleSave = async () => {
    const data = await saveInspection(vehicleId, 'assembly', params);
    alert(data.message);
  };

  return (
    <div className="space-y-4">
      <div className="flex gap-4">
        <input type="number" value={vehicleId} onChange={e => setVehicleId(e.target.value)} placeholder="Vehicle ID" className="border p-2 w-40" />
        <button onClick={handleCheck} className="bg-yellow-500 px-4 py-2 text-white rounded">Check Vehicle</button>
      </div>

      {params.length > 0 && (
        <>
          <table className="w-full border">
            <thead>
              <tr className="bg-blue-600 text-white">
                <th className="p-2 border">Parameter</th>
                <th className="p-2 border">Status</th>
                <th className="p-2 border">Observation</th>
              </tr>
            </thead>
            <tbody>
              {params.map((param, idx) => (
                <tr key={idx}>
                  <td className="border p-2">{param.parameter}</td>
                  <td className="border p-2">
                    <select
                      value={param.status}
                      onChange={e => {
                        const updated = [...params];
                        updated[idx].status = e.target.value;
                        setParams(updated);
                      }}
                      className="border p-1"
                    >
                      <option value="pass">Pass</option>
                      <option value="reject">Reject</option>
                    </select>
                  </td>
                  <td className="border p-2">
                    <input
                      value={param.observation}
                      onChange={e => {
                        const updated = [...params];
                        updated[idx].observation = e.target.value;
                        setParams(updated);
                      }}
                      className="w-full border p-1"
                    />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          <button onClick={handleSave} className="mt-4 bg-green-600 text-white px-6 py-2 rounded">Save Inspection</button>
        </>
      )}
    </div>
  );
}


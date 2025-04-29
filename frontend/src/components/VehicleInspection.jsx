import React, { useState } from 'react'

const presetParams = [
  "Top Ring Size", "Second Ring Gap", "Oil Ring Gap",
  "Valve Timing / Ignition Timing", "Crank Main and Small Bearing Torque",
  "Head Bolt Torque", "Crankshaft Bolt Torque", "Camshaft Bolt Torque",
  "Engine Leakage", "Abnormal Smoke, Abnormal Noise",
  "Engine Compression", "Engine Running (Hours)"
];

const BASE_URL = "http://localhost:8000/api";

function VehicleInspection() {
  const [vehicleId, setVehicleId] = useState('');
  const [params, setParams] = useState([]);

  const loadPresetParams = () => {
    const rows = presetParams.map(p => ({
      parameter: p,
      status: 'pass',
      observation: ''
    }));
    setParams(rows);
  }

  const handleSave = async () => {
    const response = await fetch(`${BASE_URL}/save_inspection/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        vehicle_id: parseInt(vehicleId),
        inspection_type: "assembly",
        parameters: params
      })
    });

    const data = await response.json();
    alert(data.message);
  }

  return (
    <div>
      <div className="mb-4 flex gap-4 items-center">
        <label className="text-lg font-medium">Vehicle ID:</label>
        <input
          type="number"
          className="p-2 border rounded w-40"
          value={vehicleId}
          onChange={e => setVehicleId(e.target.value)}
        />
        <button
          onClick={loadPresetParams}
          className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded"
        >
          Load Parameters
        </button>
      </div>

      <table className="w-full border mt-4">
        <thead className="bg-blue-800 text-white">
          <tr>
            <th className="p-2 border">Parameter</th>
            <th className="p-2 border">Status</th>
            <th className="p-2 border">Observation</th>
          </tr>
        </thead>
        <tbody>
          {params.map((param, idx) => (
            <tr key={idx} className="bg-gray-50">
              <td className="border p-2">
                <input type="text" readOnly value={param.parameter} className="w-full bg-gray-100 p-1" />
              </td>
              <td className="border p-2">
                <select
                  value={param.status}
                  onChange={e => {
                    const updated = [...params];
                    updated[idx].status = e.target.value;
                    setParams(updated);
                  }}
                  className="p-1 w-full"
                >
                  <option value="pass">Pass</option>
                  <option value="reject">Reject</option>
                </select>
              </td>
              <td className="border p-2">
                <input
                  type="text"
                  value={param.observation}
                  onChange={e => {
                    const updated = [...params];
                    updated[idx].observation = e.target.value;
                    setParams(updated);
                  }}
                  className="w-full p-1"
                />
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <button
        onClick={handleSave}
        className="mt-4 bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded"
      >
        Save Inspection
      </button>
    </div>
  )
}

export default VehicleInspection

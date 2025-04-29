const BASE_URL = "http://localhost:8000/api";

export const createVehicle = async (vehicleData) => {
  const res = await fetch(`${BASE_URL}/vehicles/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(vehicleData),
  });
  return res.json();
};

export const checkVehicle = async (vehicleId) => {
  const res = await fetch(`${BASE_URL}/check_vehicle/${vehicleId}/`);
  return res.json();
};

export const getInspection = async (vehicleId, inspectionType) => {
  const res = await fetch(`${BASE_URL}/get_inspection/${vehicleId}/${inspectionType}/`);
  return res.json();
};

export const saveInspection = async (vehicleId, inspectionType, parameters) => {
  const res = await fetch(`${BASE_URL}/save_inspection/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      vehicle_id: vehicleId,
      inspection_type: inspectionType,
      parameters
    }),
  });
  return res.json();
};

export const getAllVehicles = async () => {
  const res = await fetch(`${BASE_URL}/vehicles/`);
  return res.json();
};

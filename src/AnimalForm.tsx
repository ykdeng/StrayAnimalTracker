import React, { useState } from 'react';

interface AnimalFormData {
  latitude: string;
  longitude: string;
  description: string;
  photo: File | null;
}

const AnimalForm: React.FC = () => {
  const [formData, setFormData] = useState<AnimalFormData>({
    latitude: '',
    longitude: '',
    description: '',
    photo: null,
  });

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value, files } = e.target;
    setFormData({
      ...formData,
      [name]: files ? files[0] : value,
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const data = new FormData();

    // Append fields to the form data
    Object.entries(formData).forEach(([key, value]) => {
      if (value !== null) {
        data.append(key, value);
      }
    });

    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/animals`, {
        method: 'POST',
        body: data,
      });

      if (!response.ok) {
        throw new Error('There was an issue with the server.');
      }

      // Handle success
      alert('Animal sighting logged successfully!');
      setFormData({
        latitude: '',
        longitude: '',
        description: '',
        photo: null,
      });
    } catch (error) {
      alert('Failed to log animal sighting.');
      console.error(error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label htmlFor="latitude">Latitude:</label>
        <input
          type="text"
          id="latitude"
          name="latitude"
          value={formData.latitude}
          onChange={handleChange}
          required
        />
      </div>
      <div>
        <label htmlFor="longitude">Longitude:</label>
        <input
          type="text"
          id="longitude"
          name="longitude"
          value={formData.longitude}
          onChange={handleChange}
          required
        />
      </div>
      <div>
        <label htmlFor="description">Description:</label>
        <textarea
          id="description"
          name="description"
          value={formData.description}
          onChange={handleChange}
          required
        />
      </div>
      <div>
        <label htmlFor="photo">Photo:</label>
        <input
          type="file"
          id="photo"
          name="photo"
          onChange={handleChange}
        />
      </div>
      <button type="submit">Submit</button>
    </form>
  );
};

export default AnimalForm;
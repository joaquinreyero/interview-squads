import React, { useState } from 'react';
import axios from 'axios';

export const Form = () => {
  const [formData, setFormData] = useState({
    textField: '',
    videoFile: null,
    photoFile: null,
    documentFile: null,
    audioFile: null,
  });

  const handleChange = (e) => {
    const { name, value, files } = e.target;
    if (files) {
      setFormData({
        ...formData,
        [name]: files[0],
      });
    } else {
      setFormData({
        ...formData,
        [name]: value,
      });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const data = new FormData();
    data.append('text_field', formData.textField);
    data.append('video_file', formData.videoFile);
    data.append('photo_file', formData.photoFile);
    data.append('document_file', formData.documentFile);
    data.append('audio_file', formData.audioFile);

    try {
      const response = await axios.post(`${import.meta.env.VITE_BACKEND_URL}/api/example/upload`, data, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      console.log('Response:', response.data);
    } catch (error) {
      console.error('Error uploading files:', error);
    }
  };

  return (
    <div className="max-w-md mx-auto mt-10">
      <form onSubmit={handleSubmit} className="bg-white p-8 rounded-lg shadow-md">
        <h2 className="text-2xl font-bold mb-6">Formulario</h2>
        <div className="mb-4">
          <label className="block text-gray-700">Texto</label>
          <input
            type="text"
            name="textField"
            value={formData.textField}
            onChange={handleChange}
            className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-blue-500"
          />
        </div>

        <div className="mb-4">
          <label className="block text-gray-700">Video</label>
          <input
            type="file"
            name="videoFile"
            accept="video/*"
            onChange={handleChange}
            className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-blue-500"
          />
        </div>

        <div className="mb-4">
          <label className="block text-gray-700">Foto</label>
          <input
            type="file"
            name="photoFile"
            accept="image/*"
            onChange={handleChange}
            className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-blue-500"
          />
        </div>

        <div className="mb-4">
          <label className="block text-gray-700">Archivo</label>
          <input
            type="file"
            name="documentFile"
            onChange={handleChange}
            className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-blue-500"
          />
        </div>

        <div className="mb-4">
          <label className="block text-gray-700">Audio</label>
          <input
            type="file"
            name="audioFile"
            accept="audio/*"
            onChange={handleChange}
            className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-blue-500"
          />
        </div>

        <button
          type="submit"
          className="w-full bg-blue-500 text-white py-2 rounded-lg hover:bg-blue-600"
        >
          Enviar
        </button>
      </form>
    </div>
  );
};

export default Form;

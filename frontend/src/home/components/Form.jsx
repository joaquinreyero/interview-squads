import React, { useState } from 'react';
import axios from 'axios';

export const Form = () => {
  const [reelLink, setReelLink] = useState('');
  const [blogPost, setBlogPost] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    setReelLink(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await axios.post(`${import.meta.env.VITE_BACKEND_URL}/api/generate_blog_post`, { link: reelLink });
      setBlogPost(response.data);
    } catch (error) {
      setError('Error generating blog post');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto mt-10">
      <form onSubmit={handleSubmit} className="bg-white p-8 rounded-lg shadow-md">
        <h2 className="text-2xl font-bold mb-6">Instagram Reel Link</h2>
        <div className="mb-4">
          <label className="block text-gray-700">Reel Link</label>
          <input
            type="text"
            value={reelLink}
            onChange={handleChange}
            className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-blue-500"
          />
        </div>
        <button
          type="submit"
          className="w-full bg-blue-500 text-white py-2 rounded-lg hover:bg-blue-600"
        >
          Submit
        </button>
      </form>

      {loading && <p className="mt-4 text-blue-500">Generating blog post...</p>}
      {error && <p className="mt-4 text-red-500">{error}</p>}
      {blogPost && (
        <div className="mt-6 bg-gray-100 p-4 rounded-lg">
          <h3 className="text-xl font-bold mb-2">{blogPost.title}</h3>
          <p>{blogPost.content}</p>
        </div>
      )}
    </div>
  );
};

export default Form;

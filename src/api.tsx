import axios from 'axios';
import dotenv from 'dotenv';
dotenv.config();

const BASE_API_URL = process.env.REACT_APP_API_URL;

interface StrayAnimal {
  id: number;
  name: string;
  type: string;
  location: string;
  spottedAt: Date;
}

interface NewAnimalSighting {
  name: string;
  type: string;
  location: string;
  spottedAt: Date;
}

const apiClient = axios.create({
  baseURL: BASE_API_URL,
});

export const fetchStrayAnimals = async (): Promise<StrayAnimal[]> => {
  try {
    const response = await apiClient.get<StrayAnimal[]>('/stray-animals');
    return response.data;
  } catch (error) {
    console.error('Error fetching stray animals:', error);
    throw error;
  }
};

export const submitNewAnimalSighting = async (sighting: NewAnimalSighting): Promise<void> => {
  try {
    await apiClient.post('/new-sighting', sighting);
  } catch (error) {
   console.error('Error submitting new sighting:', error);
    throw error;
  }
};
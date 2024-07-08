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
export const fetchStrayAnimals = async (): Promise<StrayAnimal[]> => {
  try {
    const response = await axios.get(`${BASE_API_URL}/stray-animals`);
    return response.data;
  } catch (error) {
    console.error('Error fetching stray animals:', error);
    throw error;
  }
};
export const submitNewAnimalSighting = async (sighting: NewAnimalSighting): Promise<void> => {
  try {
    await axios.post(`${BASE_API_URL}/new-sighting`, sighting);
    console.log('Sighting submitted successfully');
  } catch (error) {
   console.error('Error submitting new sighting:', error);
    throw error;
  }
};
// apiService.ts
import axios from 'axios';

interface Animal {
  id: string;
  name: string;
  location: string;
}

async function fetchAnimalDetails(id: string): Promise<Animal> {
  const response = await axios.get(`https://api.straytrackers.com/animals/${id}`);
  return response.data;
}

async function showAnimalDetails() {
  const animalId = '123';
  const animalDetails = await fetchAnimalDetails(animalId);
  console.log(animalDetails);
}
```

```typescript
// apiService.ts
import axios from 'axios';

interface Animal {
  id: string;
  name: string;
  location: string;
}

async function fetchAnimalsDetails(ids: string[]): Promise<Animal[]> {
  const response = await axios.get(`https://api.straytrackers.com/animals`, {
    params: { ids: ids.join(',') },
  });
  return response.data;
}

async function fetchAnimalsDetailsInBatches(ids: string[], batchSize: number) {
  let batchedAnimals: Animal[] = [];
  for (let i = 0; i < ids.length; i += batchSize) {
    const batchIds = ids.slice(i, i + batchSize);
    const animalsDetails = await fetchAnimalsDetails(batchIds);
    batchedAnimals = batchedAnimals.concat(animalsDetails);
  }
  return batchedAnimals;
}

async function showMultipleAnimalsDetails() {
  const animalIds = ['123', '456', '789', '101112'];
  const animalsDetails = await fetchAnimalsDetailsInBatches(animalIds, 2);
  console.log(animalsDetails);
}
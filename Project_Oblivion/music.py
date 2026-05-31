from sklearn.neighbors import NearestNeighbors
from sentence_transformers import SentenceTransformer
from sklearn.decomposition import PCA
import numpy as np 
import random 
from textual import work
import re

import threading
from Project_Oblivion.core import initialize_vault


class Loom():
    def __init__(self):
        file_path = initialize_vault()
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        with open(file_path, "r") as f: 
            self.atoms = [line.strip() for line in f if line.strip()]
        self.clean_atoms = []
        for atom in self.atoms:
            if "|" in atom:
                content = atom.split("|")[-1].strip()
                self.clean_atoms.append(content)
            else:
                self.clean_atoms.append(atom.strip()) 


        self.embeddings = self.model.encode(self.clean_atoms, convert_to_numpy=True, normalize_embeddings=True)

        self.knn = NearestNeighbors(n_neighbors=5, metric='cosine')
        self.knn.fit(self.embeddings)
    def coords(self):

        pca = PCA(n_components=2)
        coords = pca.fit_transform(self.embeddings)
        x_coords = coords[:, 0].tolist()
        y_coords = coords[:,1].tolist()
        return {"x": x_coords, "y":y_coords}
    


    def get_related_atoms(self,input_index):
        # Get the vector for the selected atom
        query_vector = self.embeddings[input_index].reshape(1, -1)
        
        # Find indices of the nearest neighbors
        distances, indices = self.knn.kneighbors(query_vector)
        
        print(f"Original Atom: {self.clean_atoms[input_index]}")
        print("-" * 20)
        
        # The first result is always the atom itself, so we look at the subsequent ones
        for i in range(1, len(indices[0])):
            neighbor_idx = indices[0][i]
            return f"Linked Connection: {self.clean_atoms[neighbor_idx]} (Distance: {distances[0][i]:.4f})"

    # Test it with the "Mistakes" atom


    def whisper_connection(self):
        try: 
            idx = random.randint(0, len(self.clean_atoms) - 1)
            query_vec = self.embeddings[idx].reshape(1,-1)

            distance, indices = self.knn.kneighbors(query_vec, n_neighbors=5)
            print(f"Whisper (Original): {self.atoms[idx]}")
            print("-" * 30)

            for i in range(1, len(indices[0])):
                n_idx = indices[0][i]
                strength = 1 - distance[0][i]
                # Ensure you are referencing the original 'atoms' list
                print(f"Linked Connections: {self.atoms[n_idx]} (Strength: {strength:.4f})")
                return {"whisper": self.atoms[n_idx][0]}
        except ValueError:
            raise ValueError("Something wrong happened.")


    def query(self,inputs):
        try:
            query_vec = self.model.encode(inputs).reshape(1, -1)
            distance, indices = self.knn.kneighbors(query_vec, n_neighbors=5)
            print(f"Query(Original): {inputs}")
            for i in range(1, len(indices[0])):
                n_idx = indices[0][i]
                strenght = 1 - distance[0][i]
                print(f"Links COnnections: {self.atoms[n_idx]} (Strenght: {strenght:.4f})")
        except ValueError:
            print(f"'{inputs}' not found in atoms.")
        



def load():
    loom = Loom()
    return loom

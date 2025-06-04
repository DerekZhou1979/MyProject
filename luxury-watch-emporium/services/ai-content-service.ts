
import { GoogleGenAI, GenerateContentResponse } from "@google/genai";
import { Product } from '../types';
import { GEMINI_MODEL_TEXT, API_KEY_ERROR_MESSAGE } from '../seagull-brand-config.tsx';

let ai: GoogleGenAI | null = null;
const API_KEY = process.env.API_KEY;

if (API_KEY && API_KEY.trim() !== "") {
  try {
    ai = new GoogleGenAI({ apiKey: API_KEY });
  } catch (error) {
    console.error("Failed to initialize GoogleGenAI client:", error);
    // ai remains null, subsequent calls to geminiService will return API_KEY_ERROR_MESSAGE
  }
} else {
  // Log to console, user will see API_KEY_ERROR_MESSAGE in UI when feature is used.
  console.warn(API_KEY_ERROR_MESSAGE + " Gemini-related features will be unavailable or show an error message in the UI.");
}

export const geminiService = {
  generateCreativeDescription: async (product: Product): Promise<string> => {
    if (!ai) { // Check if ai was initialized successfully
      // This also covers the case where API_KEY was missing.
      return API_KEY_ERROR_MESSAGE;
    }
    try {
      const prompt = `Generate a short, poetic and stylish insight (max 50 words, one paragraph) for a luxury watch named "${product.name}" from the "${product.category}" collection. Key features: ${product.features.join(', ')}. Emphasize its elegance, craftsmanship, and appeal to a young, discerning audience. Do not use markdown or bullet points in the response.`;
      
      const response: GenerateContentResponse = await ai.models.generateContent({
        model: GEMINI_MODEL_TEXT,
        contents: prompt,
        config: {
            temperature: 0.7,
            topP: 0.9,
            topK: 40,
        }
      });
      
      // Correctly access the text property
      const text = response.text;
      return text.trim();

    } catch (error) {
      console.error("Error generating creative description with Gemini:", error);
      // Check if the error is due to API key specifically, if possible, or provide a general error.
      // The SDK might throw errors with specific codes or messages for auth issues.
      if (error instanceof Error) {
        const errorMessage = error.message.toLowerCase();
        if (errorMessage.includes("api key") || 
            errorMessage.includes("permission denied") || 
            errorMessage.includes("authentication") ||
            errorMessage.includes("quota") ||
            (error.name && error.name.toLowerCase().includes("google"))) { // Broader check for Google API errors
           return API_KEY_ERROR_MESSAGE + " (Details: " + error.message + ")";
        }
      }
      return "Could not generate a creative insight at this time. Please try again later.";
    }
  },
};

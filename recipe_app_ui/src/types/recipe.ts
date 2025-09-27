export type Recipe = {
  id: number;
  name: string;
  cuisine: string;
  difficulty: string;
  servings: number;
  prep_time_minutes: number;
  cook_time_minutes: number;
  calories_per_serving?: number;
  user_id?: number;
  image?: string;
  rating?: number;
  review_count?: number;

  // flattened relations
  ingredients: string[];
  tags: string[];
  meal_types: string[];
  instructions: string[];
};
export type Recipe = {
  id: number;
  name: string;
  cuisine: string;
  difficulty: string;
  servings: number;
  prep_time_minutes: number;
  cook_time_minutes: number;
  calories_per_serving?: number;
  image?: string;
  tags?: string[];
};

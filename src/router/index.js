import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import AddMovieFormView from '../views/AddMovieFormView.vue';
import MoviesView from '../views/MoviesView.vue'; // 👈 new import

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue')
    },
    {
      path: '/movies/create',
      name: 'add-movie',
      component: AddMovieFormView
    },
    {
      path: '/movies',
      name: 'movies',
      component: MoviesView // 👈 route for movie gallery
    }
  ]
});

export default router;

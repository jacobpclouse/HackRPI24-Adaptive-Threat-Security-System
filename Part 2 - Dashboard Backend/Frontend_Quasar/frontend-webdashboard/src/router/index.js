import { createRouter, createWebHistory } from 'vue-router';
import routes from './routes';

const Router = createRouter({
  history: createWebHistory(),
  routes
});

Router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token');
  
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!token) {
      next('/login');  // Redirect to login if not authenticated
    } else {
      next();  // Proceed to dashboard if authenticated
    }
  } else {
    next();  // If route doesn't require auth, proceed
  }
});

export default Router;

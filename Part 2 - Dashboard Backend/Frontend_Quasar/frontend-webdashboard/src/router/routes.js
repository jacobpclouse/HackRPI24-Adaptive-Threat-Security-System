const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { 
        path: 'dashboard', 
        component: () => import('pages/DashboardPage.vue'), 
        name: 'dashboard',  // Adding a name for easy reference
        meta: { requiresAuth: true }
      },
      { 
        path: '', 
        component: () => import('pages/IndexPage.vue'), 
        name: 'index',  // Adding a name for easy reference
        meta: { requiresAuth: true }
      },
      { 
        path: 'video/:id',  // Remove the leading slash
        component: () => import('pages/VideoPage.vue'), 
        name: 'video',  // Set the name to match what you're using in `push`
        meta: { requiresAuth: true }
      },
      { path: 'signup', component: () => import('pages/SignupPage.vue'), name: 'signup' },
      { path: 'login', component: () => import('pages/LoginPage.vue'), name: 'login' }
    ]
  }
];

export default routes;


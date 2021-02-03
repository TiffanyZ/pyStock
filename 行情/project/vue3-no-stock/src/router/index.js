import { createRouter, createWebHashHistory } from "vue-router";
import All from "../views/Home.vue";

const routes = [
  {
    path: "/",
    name: "All",
    component: All
  },
  {
    path: "/per",
    name: "Per",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "All" */ "../views/Per.vue")
  },
  {
    path: "/list",
    name: "List",
    component: () => import(/* webpackChunkName: "List" */ "../views/List.vue")
  }
];

const router = createRouter({
  history: createWebHashHistory(),
  routes
});

export default router;

import { createStore } from 'vuex';
import auth from './modules/auth';
// import hosts from './modules/hosts';
// import containers from './modules/containers';

export default createStore({
  modules: {
    auth,
    // hosts,
    // containers
  }
});
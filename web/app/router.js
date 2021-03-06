import Ember from 'ember';
import config from './config/environment';

const Router = Ember.Router.extend({
  location: config.locationType
});

Router.map(function() {
  this.route('characters', function() {
    this.route('show', { path: '/:character_lid' });
  });
  this.route('servers', function() {
    this.route('show', { path: '/:server_slug' });
  });
  this.route('grand-companies', function() {
    this.route('show', { path: '/:gc_slug' });
  });
  this.route('races', function() {});
});

export default Router;

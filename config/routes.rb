Rails.application.routes.draw do
  namespace :api do
    namespace :v1 do
      resources :tasks
      resources :confidentials
      resources :cars
      resources :refuelings
      resources :notes
    end
  end
end

Rails.application.routes.draw do
  namespace :api do
    namespace :v1 do
      resources :tasks
      resources :task_lists
      resources :confidentials
      resources :cars
      resources :refuelings
      resources :notes
    end
  end
end

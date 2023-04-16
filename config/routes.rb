Rails.application.routes.draw do
  namespace :api do
    namespace :v1 do
      resources :tasks
      resources :auth_infos
    end
  end
end

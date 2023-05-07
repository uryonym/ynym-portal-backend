Rails.application.routes.draw do
  namespace :api do
    namespace :v1 do
      resources :tasks, except: [:show]
      resources :auth_infos, except: [:show]
    end
  end
end

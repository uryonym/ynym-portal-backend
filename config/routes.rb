Rails.application.routes.draw do
  namespace :api do
    namespace :v1 do
      resources :tasks, except: [:show]
      resources :auth_infos, except: [:show]
      resources :cars, except: [:show]
      resources :refuelings, except: [:show]
    end
  end
end

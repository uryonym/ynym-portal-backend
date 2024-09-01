# frozen_string_literal: true

Rails.application.routes.draw do
  namespace :api do
    namespace :v1 do
      resources :tasks
      resources :confidentials
      resources :cars do
        resources :refuelings
      end
      resources :notes do
        resources :sections do
          resources :pages
        end
      end
    end
  end
end

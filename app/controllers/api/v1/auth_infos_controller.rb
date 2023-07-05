class Api::V1::AuthInfosController < ApplicationController
  def index
    auth_infos = AuthInfo.order(:created_at)
    render json: auth_infos
  end

  def create
    auth_info = AuthInfo.new(auth_info_params)
    if auth_info.save
      render json: auth_info
    else
      render json: auth_info.errors
    end
  end

  def show
    auth_info = AuthInfo.find(params[:id])
    render json: auth_info
  end

  def update
    auth_info = AuthInfo.find(params[:id])
    if auth_info.update(auth_info_params)
      render json: auth_info
    else
      render json: auth_info.errors
    end
  end

  def destroy
    auth_info = AuthInfo.find(params[:id])
    auth_info.destroy
    render json: auth_info
  end

  private def auth_info_params
    params.require(:auth_info).permit(
      :id,
      :service_name,
      :login_id,
      :password,
      :other,
      :created_at,
      :updated_at
    )
  end
end

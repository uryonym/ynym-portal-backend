class Api::V1::PagesController < ApplicationController
  skip_before_action :authenticate_token

  def index
    pages = Page.order(:seq)
    render json: pages
  end

  def create
    page = Page.new(page_params)
    if page.save
      render json: page
    else
      render json: page.errors
    end
  end

  def show
    page = Page.find(params[:id])
    render json: page
  end

  def update
    page = Page.find(params[:id])
    if page.update(page_params)
      render json: page
    else
      render json: page.errors
    end
  end

  def destroy
    page = Page.find(params[:id])
    page.destroy
    render json: page
  end

  private def page_params
    params.require(:page).permit(:id, :title, :content, :uid, :seq, :section_id)
  end
end

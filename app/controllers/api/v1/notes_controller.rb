class Api::V1::NotesController < ApplicationController
  skip_before_action :authenticate_token

  def index
    notes = Note.order(:created_at)
    render json: notes
  end

  def create
    note = Note.new(note_params)
    if note.save
      render json: note
    else
      render json: note.errors
    end
  end

  def show
    note = Note.find(params[:id])
    render json: note
  end

  def update
    note = Note.find(params[:id])
    if note.update(note_params)
      render json: note
    else
      render json: note.errors
    end
  end

  def destroy
    note = Note.find(params[:id])
    note.destroy
    render json: note
  end

  private def note_params
    params.require(:note).permit(
      :id,
      :title,
      :content,
      :created_at,
      :updated_at
    )
  end
end

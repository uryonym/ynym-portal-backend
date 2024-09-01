# frozen_string_literal: true

class Api::V1::NotesController < ApplicationController
  def index
    notes = Note.where(uid: @current_user.uid).order(:seq)
    render(json: notes)
  end

  def create
    note = Note.new(note_params)
    note.uid = @current_user.uid
    if note.save
      render(json: note)
    else
      render(json: note.errors, status: :unprocessable_entity)
    end
  end

  def show
    note = Note.find(params[:id])
    render(json: note)
  end

  def update
    note = Note.find(params[:id])
    if note.update(note_params)
      render(json: note)
    else
      render(json: note.errors, status: :unprocessable_entity)
    end
  end

  def destroy
    note = Note.find(params[:id])
    note.destroy
    render(json: note)
  end

  private def note_params
    params.require(:note).permit(:id, :name, :seq)
  end
end
